# image_processor

## Overview
This Django-based application processes image data provided via a CSV file. The system asynchronously processes the images by compressing them and storing the processed images alongside the original image URLs in a database. It also provides APIs for uploading the CSV file, checking the processing status, and triggering webhooks upon completion.

## Features
CSV Upload: Accepts a CSV file containing product information and image URLs.__
Validation: Validates the CSV file format and content.__
Asynchronous Processing: Compresses images asynchronously by 50% of their original quality.__
Database Storage: Stores the processed images and associated product information in a SQLite database.__
API Endpoints:__
Upload API: Accepts the CSV file and returns a unique request ID.__
Status API: Allows users to query the processing status using the request ID.__
Webhook Trigger: Triggers a webhook after all images are processed.__

### Installation
Prerequisites_
Python 3.8+
Django 3.x+
RabbitMQ
djangorestframework
celery
boto3
pillow
