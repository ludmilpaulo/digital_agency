# core/models.py

from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=100)
    quote = models.TextField()
    avatar = models.ImageField(upload_to='avatar/',blank=True, null=True)
    stars = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.role})"
