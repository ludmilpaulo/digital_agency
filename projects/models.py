from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.title
