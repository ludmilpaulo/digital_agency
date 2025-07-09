from django.db import models
from django.contrib.auth import get_user_model
import jsonfield

User = get_user_model()

class GoogleCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credentials = jsonfield.JSONField()
