from django.db import models

class Upload(models.Model):
    request_id = models.CharField(max_length=255, unique=True)
    file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=50, default='pending')  
    created_at = models.DateTimeField(auto_now_add=True)
    webhook_url = models.URLField(null=True, blank=True)

class ProcessedImage(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    original_url = models.URLField()
    processed_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

