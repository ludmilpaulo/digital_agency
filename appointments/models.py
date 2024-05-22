from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
