from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Solution(models.Model):
    name = models.CharField(max_length=200)
    description = CKEditor5Field()
    image = models.ImageField(upload_to='solutions/')
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
