from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    # add more fields here as needed