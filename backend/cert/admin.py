from django.contrib import admin

# Register your models here.
from .models import Cert


class CertAdmin(admin.ModelAdmin):
    list_display = ("id", "certDataString", "lastUpdatedAt", "nonce")


# Register your models here.

admin.site.register(Cert, CertAdmin)
