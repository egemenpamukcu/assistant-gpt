from django.db import models

# Create your models here.
class Bot(models.Model):
    prompt = models.CharField(max_length=10000)

    def __str__(self):
        return self.prompt