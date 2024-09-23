"""DRF Analyses viewset"""

# Lib imports
import json
import os
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

# App imports
from myapp.models import Analysis
from myapp.resources.analyses.serializer import AnalysisSerializer
from myapp.scripts.dinkey_methods import ProtCheck

class AnalysisViewSet(viewsets.ModelViewSet):
    """Analysis viewset"""

    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

    def create(self, request, *args, **kwargs):
        """Override obj create"""
        # check protection
        ret_val = ProtCheck()
        if  ret_val != 0:
            # we may just as well raise an UNAUTHORIZED error
            return Response({"message": "Dongle is not connected. Analyses creation not allowed"})
        return super().create(request, *args, *kwargs)
