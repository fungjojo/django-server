from rest_framework import serializers
from .models import Cert
from .services import CertLogicService
from django.db import models


class CertSerializer(serializers.ModelSerializer):
    # def create(self):
    #     data = CertLogicService.issue_cert(self.request)
    #     return Model.obj
    class Meta:
        model = Cert
        fields = ("id", "certDataString", "lastUpdatedAt", "nonce")
