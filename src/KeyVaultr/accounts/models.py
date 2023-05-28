from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField()
    master_pin = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.username
    