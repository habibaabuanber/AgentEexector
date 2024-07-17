from rest_framework import serializers
from .models import FileDescription

class FileDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileDescription
        fields = ['file_name', 'description']
