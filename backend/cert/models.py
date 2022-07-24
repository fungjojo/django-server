from django.db import models

# Create your models here.


class Cert(models.Model):
    # id = models.CharField(max_length=120, primary_key=True)
    certDataString = models.CharField(max_length=30000)
    lastUpdatedAt = models.DateTimeField()
    userId = models.CharField(max_length=30000)
    txnId = models.CharField(max_length=30000, blank=True, default="")
    nonce = models.IntegerField(blank=True, default=0)

    def _str_(self):
        return self.id
