from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CertSerializer
from .models import Cert

# Create your views here.

class CertView(viewsets.ModelViewSet):
    serializer_class = CertSerializer
    queryset = Cert.objects.all()