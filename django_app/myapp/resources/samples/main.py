"""DRF File viewset"""

# Lib imports
import json
import os
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

# App imports
from myapp.models import Sample
from myapp.resources.samples.serializer import SampleSerializer
from myapp.scripts.dinkey_methods import ProtCheck

class SampleViewSet(viewsets.ModelViewSet):
    """File viewset"""

    queryset = Sample.objects.all()
    serializer_class = SampleSerializer

    def create(self, request, *args, **kwargs):
        """Override obj create"""
        # check protection
        ret_val = ProtCheck()
        if  ret_val != 0:
            return Response({"message": "Dongle is not connected. Sample creation not allowed"})
        return super().create(request, *args, **kwargs)

    