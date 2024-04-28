from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Service(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    description = CKEditor5Field('Text', config_name='extends')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.title
