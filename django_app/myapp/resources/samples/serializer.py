"""DRF Sample serializer"""

from rest_framework import serializers

# App imports
from myapp.models import Sample


class SampleSerializer(serializers.ModelSerializer):
    """Sample serializer class"""

    class Meta:
        model = Sample
        fields = ['id', 'name', 'analysis']