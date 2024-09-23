"""DRF Analyses serializer"""

from rest_framework import serializers

# App imports
from myapp.models import Analysis
from myapp.resources.samples.serializer import SampleSerializer
from myapp.resources.files.serializer import FileSerializer


class AnalysisSerializer(serializers.Serializer):
    """Analyses serializer class"""

    samples = SampleSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Analysis
        fields = ['id', 'name', 'samples', 'files']