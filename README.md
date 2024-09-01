# image_processor

## Overview
This Django-based application processes image data provided via a CSV file. The system asynchronously processes the images by compressing them and storing the processed images alongside the original image URLs in a database. It also provides APIs for uploading the CSV file, checking the processing status, and triggering webhooks upon completion.

## Features
CSV Upload: Accepts a CSV file containing product information and image URLs.<br>
Validation: Validates the CSV file format and content.<br>
Asynchronous Processing: Compresses images asynchronously by 50% of their original quality.<br>
Database Storage: Stores the processed images and associated product information in a SQLite database.<br>
API Endpoints:<br>
Upload API: Accepts the CSV file and returns a unique request ID.<br>
Status API: Allows users to query the processing status using the request ID.<br>
Webhook Trigger: Triggers a webhook after all images are processed.<br>

### Installation
Prerequisites<br>
Python 3.8+<br>
Django 3.x+<br>
RabbitMQ<br>
djangorestframework<br>
celery<br>
boto3<br>
pillow<br>
