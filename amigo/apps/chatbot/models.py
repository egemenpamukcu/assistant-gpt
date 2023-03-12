from django.db import models

class Bot(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    prompt = models.TextField(blank=False, null=False)