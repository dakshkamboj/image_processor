import csv
import uuid
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Upload, ProcessedImage
from .serializers import UploadSerializer, ProcessedImageSerializer
from .tasks import process_images_task
import csv
import re
from io import StringIO
from django.core.exceptions import ValidationError

class UploadView(APIView):
    def post(self, request, format=None):
        file = request.FILES.get('file')
        webhook_url = request.data.get('webhook_url')

        if not file:
            return Response({"error": "CSV file is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_csv_file(file)
        except Exception as e:
            return Response({"error": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        upload = Upload.objects.create(request_id=request_id, file=file, webhook_url=webhook_url)
        
        # Start the asynchronous image processing task
        process_images_task.delay(upload.id)
        
        return Response({"request_id": request_id}, status=status.HTTP_201_CREATED)



def validate_csv_file(file):
    required_columns = ['S.No.', 'Product Name', 'Input Image Urls']
    
    try:
        file_data = file.read().decode('utf-8')
        csv_reader = csv.DictReader(StringIO(file_data))
    except Exception as e:
        raise ValidationError(f"Invalid CSV file: {e}")
    
    # Validate header
    if not set(required_columns).issubset(csv_reader.fieldnames):
        raise ValidationError("CSV file is missing required columns.")
    
    url_pattern = re.compile(r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$')

    # Validate rows
    for row_number, row in enumerate(csv_reader, start=1):
        if not row['S.No.']:
            raise ValidationError(f"Missing 'Serial Number' in row {row_number}.")
        
        if not row['Product Name']:
            raise ValidationError(f"Missing 'Product Name' in row {row_number}.")
        
        if not row['Input Image Urls']:
            raise ValidationError(f"Missing 'Input Image Urls' in row {row_number}.")
        
        image_urls = [url.strip() for url in row['Input Image Urls'].split(',')]
        
        for url in image_urls:
            if not url_pattern.match(url):
                raise ValidationError(f"Invalid URL '{url}' in row {row_number}.")

    return True


class StatusView(APIView):
    def get(self, request, request_id, format=None):
        upload = get_object_or_404(Upload, request_id=request_id)
        serializer = UploadSerializer(upload)
        return Response(serializer.data)
