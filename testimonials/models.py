from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clients_logos/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners_logos/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    testimonial = models.TextField()
    image = models.ImageField(upload_to='testimonials/')

    def __str__(self):
        return f"{self.name} - {self.designation}"