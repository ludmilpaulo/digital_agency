from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth import get_user_model
User = get_user_model()

class Board(models.Model):
    name = models.CharField(max_length=100)
    description = CKEditor5Field('Text', config_name='extends')
    development_link = models.URLField(max_length=500, blank=True)
    repository_link = models.URLField(max_length=500, blank=True)
    client_link = models.URLField(max_length=500, blank=True)
    sample_link = models.URLField(max_length=500, blank=True)
    users = models.ManyToManyField(User, related_name='boards', db_column='user_id')  # Specify db_column if necessary
    managers = models.ManyToManyField(User, related_name='managed_boards', db_column='manager_id')
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_used = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Started', 'Started'),
        ('In Progress', 'In Progress'),
        ('Concluded', 'Concluded')
    ], default='Started')

    def __str__(self):
        return self.name





class List(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, related_name='lists', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Card(models.Model):
    title = models.CharField(max_length=100)
    description = CKEditor5Field('Text', config_name='extends')
    status = models.CharField(max_length=100, default='Not Started')  # Not Started, In Progress, Completed
    list = models.ForeignKey('List', related_name='cards', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='card_images/', blank=True, null=True)  # Add image field

    def __str__(self):
        return self.title
