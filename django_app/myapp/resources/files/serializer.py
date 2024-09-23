"""DRF Analyses serializer"""

from rest_framework import serializers

# App imports
from myapp.models import File


class FileSerializer(serializers.ModelSerializer):
    """Analyses serializer class"""

    class Meta:
        model = File
        fields = ['id', 'path', 'uri', 'url', 'tags', 'size', 'analysis']