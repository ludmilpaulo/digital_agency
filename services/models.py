from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth import get_user_model
User = get_user_model()

class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='category/', blank=True)
    slug = models.SlugField(max_length=200, blank=True,
                            unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'Service category'
        verbose_name_plural = 'Service categories'
    def __str__(self):
        return self.name




class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, related_name='service', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(max_length=3000, default=None, blank=True, upload_to='service_images/')
    rating = models.IntegerField(default=0)
    description = CKEditor5Field()


    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Service'

    def __str__(self):
        return self.title





class ServiceRequest(models.Model):
    service = models.ForeignKey(Service, related_name='requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"