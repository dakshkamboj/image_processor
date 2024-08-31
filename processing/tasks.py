import csv
import requests
import uuid
from PIL import Image
from io import BytesIO
from celery import shared_task
from django.conf import settings
from .models import Upload, ProcessedImage
import boto3

s3 = boto3.client('s3')

@shared_task
def process_images_task(upload_id):
    upload = Upload.objects.get(id=upload_id)
    upload.status = 'in_progress'
    upload.save()

    try:
        # Read the CSV file
        file_path = upload.file.path
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                product_name = row['Product Name']
                image_urls = row['Input Image Urls'].split(',')

                for image_url in image_urls:
                    response = requests.get(image_url.strip())
                    img = Image.open(BytesIO(response.content))

                    # Compress the image to 50%
                    img_io = BytesIO()
                    img.save(img_io, format='JPEG', quality=50)
                    img_io.seek(0)

                    # Generate a file name and upload to S3
                    file_name = f"{uuid.uuid4()}.jpg"
                    s3.upload_fileobj(
                        img_io,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        file_name,
                        ExtraArgs={'ContentType': 'image/jpeg'}
                    )
                    
                    processed_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}"

                    # Save processed image info to database
                    ProcessedImage.objects.create(
                        upload=upload,
                        product_name=product_name,
                        original_url=image_url.strip(),
                        processed_url=processed_url
                    )

        upload.status = 'completed'

        if upload.webhook_url:
            trigger_webhook(upload)

    except Exception as e:
        upload.status = 'failed'
        print(f"Error processing images: {e}")
    finally:
        upload.save()


def trigger_webhook(upload):
    """
    Sends a POST request to the webhook URL with the processed data.
    """
    processed_images = ProcessedImage.objects.filter(upload=upload)
    data = {
        "request_id": upload.request_id,
        "status": upload.status,
        "processed_images": [
            {
                "product_name": image.product_name,
                "original_url": image.original_url,
                "processed_url": image.processed_url,
            }
            for image in processed_images
        ],
    }
    
    try:
        response = requests.post(upload.webhook_url, json=data)
        response.raise_for_status()
        print(f"Webhook triggered successfully: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to trigger webhook: {e}")