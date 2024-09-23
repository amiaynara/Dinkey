"""DRF Analyses viewset"""

# Lib imports
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

# App imports
from myapp.models import File
from myapp.resources.files.serializer import FileSerializer

class FileViewSet(viewsets.ModelViewSet):
    """Analyses viewset"""

    queryset = File.objects.all()
    serializer_class = FileSerializer
    