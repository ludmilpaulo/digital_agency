from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.title
class ProjectInquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    company = models.CharField(max_length=200, blank=True)
    project = models.CharField(max_length=300)
    budget = models.CharField(max_length=100)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.project}"