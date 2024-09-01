# image_processor

## Overview

This Django-based application processes image data provided via a CSV file. The system asynchronously processes the images by compressing them and storing the processed images alongside the original image URLs in a database. It also provides APIs for uploading the CSV file, checking the processing status, and triggering webhooks upon completion.

## Features

- **CSV Upload**: Accepts a CSV file containing product information and image URLs.
- **Validation**: Validates the CSV file format and content.
- **Asynchronous Processing**: Compresses images asynchronously by 50% of their original quality.
- **Database Storage**: Stores the processed images and associated product information in a SQLite database.
- **API Endpoints**:
  - **Upload API**: Accepts the CSV file and returns a unique request ID.
  - **Status API**: Allows users to query the processing status using the request ID.
  - **Webhook Trigger**: Triggers a webhook after all images are processed.

## Installation

### Prerequisites

- Python 3.8+
- Django 3.x+
- RabbitMQ
- djangorestframework
- celery
- boto3
- pillow

  ### Setup Instructions

1. **Clone the Repository**:

  #### Update settings file bukcet name and broker_url according to setup
   ```bash
   git clone https://github.com/dakshkamboj/image_processor.git
   cd image-processor
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py runserver IP:PORT
  ```

## Curl for upload API:
### Change the file location accordingly and path according to OS (This request is of local windows)

curl -X POST -F "file=@C://Users//Daksh//OneDrive//Desktop//test.csv" -F "webhook_url=https://your-webhook-url.com/endpoint" http://54.82.229.250:8000/api/upload

## Curl for getting status:
### Change request-id as per above API response

curl -X GET http://54.82.229.250:8000/api/status/0e9ef6ea-7318-415d-ac4a-9233da6d7d5b
