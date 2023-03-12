from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.bio:
            self.bio = self.get_default_bio()
        super().save(*args, **kwargs)

    def get_default_bio():
        return """Name: Unknown

        Age: Unknown

        Occupation: Unknown

        Interests: Unknown

        Personality traits: Unknown

        Other relevant information: Unknown."""