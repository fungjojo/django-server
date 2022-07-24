# Generated by Django 4.0.5 on 2022-06-22 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cert",
            fields=[
                (
                    "id",
                    models.CharField(max_length=120, primary_key=True, serialize=False),
                ),
                ("certDataString", models.CharField(max_length=30000)),
                ("lastUpdatedAt", models.DateTimeField()),
                ("userId", models.CharField(max_length=30000)),
                ("txnId", models.CharField(max_length=30000)),
                ("nonce", models.IntegerField()),
            ],
        ),
    ]
