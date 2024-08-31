from rest_framework import serializers
from .models import Upload, ProcessedImage

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['request_id', 'file', 'status', 'created_at']

class ProcessedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedImage
        fields = ['product_name', 'original_url', 'processed_url', 'created_at']
