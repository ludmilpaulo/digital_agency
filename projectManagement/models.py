from django.db import models

from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth import get_user_model
User = get_user_model()

from tasks.models import Board

class Project(models.Model):
    name = models.ForeignKey(Board, on_delete=models.CASCADE)
    description = CKEditor5Field('Text', config_name='extends')
    manager = models.ForeignKey(User, related_name='managed_projects', on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = CKEditor5Field('Text', config_name='extends')
    assigned_to = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed')])

class Report(models.Model):
    project = models.ForeignKey(Project, related_name='reports', on_delete=models.CASCADE)
    content = CKEditor5Field('Text', config_name='extends')
    created_at = models.DateField(auto_now_add=True)
