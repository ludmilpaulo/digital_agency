from django.db import models
from django.utils import timezone
from django.urls import reverse
import re

from django_ckeditor_5.fields import CKEditor5Field

class Image(models.Model):
    image = models.ImageField(max_length=3000, default='', blank=True, upload_to='carousel_images/')

    def __str__(self):
        return self.image.name if self.image else ''


class Carousel(models.Model):
	image = models.ManyToManyField(Image)
	title = models.CharField(max_length=150)
	sub_title = models.CharField(max_length=100)

	def __str__(self):
		return self.title


# Create your models here.

class AboutUs(models.Model):
    title = models.CharField(max_length = 50)
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    backgroundImage = models.ImageField(upload_to="Back_logo/", blank=True, null=True)
    backgroundApp = models.ImageField(upload_to="Back_logo/", blank=True, null=True)
    about = CKEditor5Field('Text', config_name='extends')
    born_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)


    class Meta:
        verbose_name = 'about us '
        verbose_name_plural = 'about us '

    def __str__(self):
        return self.title


class Why_Choose_Us(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    class Meta:
        verbose_name = 'why choose us '
        verbose_name_plural = 'why choose us '

    def __str__(self):
        return self.title


from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    bio = models.CharField(max_length=500)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)  # For 'Contact' button

    # Store tags/skills as a JSON field (PostgreSQL recommended) or as comma-separated if using SQLite
    tags = models.JSONField(blank=True, null=True, default=list)

    class Meta:
        verbose_name = 'Squad'
        verbose_name_plural = 'Squad'

    def __str__(self):
        return self.name



class Timeline(models.Model):
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=80)
    desc = models.TextField()

    class Meta:
        ordering = ["year"]

    def __str__(self):
        return f"{self.year} - {self.title}"

class Partner(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='partners/')
    url = models.URLField()

    def __str__(self):
        return self.name


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    confirm_token = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
    subject = models.CharField(max_length=50)
    from_email = models.EmailField()
    phone = models.CharField(max_length=39)
    message = models.TextField(verbose_name='Conteúdo')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp'] # most recent saved show up first
        verbose_name = 'Client contact'
        verbose_name_plural = 'Client contacts'


    def __str__(self):
        return self.subject


