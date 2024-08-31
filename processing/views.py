import csv
import uuid
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Upload, ProcessedImage
from .serializers import UploadSerializer, ProcessedImageSerializer
from .tasks import process_images_task

class UploadView(APIView):
    def post(self, request, format=None):
        file = request.FILES.get('file')
        webhook_url = request.data.get('webhook_url')

        if not file:
            return Response({"error": "CSV file is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        upload = Upload.objects.create(request_id=request_id, file=file, webhook_url=webhook_url)
        
        # Start the asynchronous image processing task
        process_images_task.delay(upload.id)
        
        return Response({"request_id": request_id}, status=status.HTTP_201_CREATED)


class StatusView(APIView):
    def get(self, request, request_id, format=None):
        upload = get_object_or_404(Upload, request_id=request_id)
        serializer = UploadSerializer(upload)
        return Response(serializer.data)
