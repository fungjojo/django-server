from rest_framework import serializers
from .models import Cert

class CertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cert
        fields = ('id', 'certDataString', 'lastUpdatedAt')