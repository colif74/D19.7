from django.db import models


# Create your models here.
class OneTimeCode(models.Model):
    objects = None
    code = models.CharField(max_length=10)
    user = models.CharField(max_length=255)