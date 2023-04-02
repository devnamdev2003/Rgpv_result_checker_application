from django.db import models

# Create your models here.


class Data(models.Model):
    name = models.CharField(max_length=200)
    roll = models.CharField(max_length=200)
    branch = models.CharField(max_length=20)
    sem = models.CharField(max_length=12)
    sgpa = models.CharField(max_length=12)
    cgpa = models.CharField(max_length=12)
    result = models.CharField(max_length=20)
