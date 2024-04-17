from django.db import models
from django.utils import timezone
from django.urls import reverse




class Carousel(models.Model):
	image = models.ImageField(upload_to='pics/%y/%m/%d/')
	title = models.CharField(max_length=150)
	sub_title = models.CharField(max_length=100)

	def __str__(self):
		return self.title


# Create your models here.

class AboutUs(models.Model):
    title = models.CharField(max_length = 50)
    content = models.TextField()


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


class Team(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    bio = models.CharField(max_length=500)
    image = models.ImageField(upload_to='chef/')    

    class Meta:
        verbose_name = 'Squad'
        verbose_name_plural = 'Squad'

    def __str__(self):
        return self.name








class Contact(models.Model):
    subject = models.CharField(max_length=50)
    from_email = models.EmailField()
    phone = models.CharField(max_length=9)
    message = models.TextField(verbose_name='Conteúdo')
   
  
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp'] # most recent saved show up first
        verbose_name = 'Client contact'
        verbose_name_plural = 'Client contacts'


    def __str__(self):
        return self.subject



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
   
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
   

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Hire '
        verbose_name_plural = 'Hire '

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:hire_detail',
                       args=[self.id, self.slug])

class Document(models.Model):
    photo = models.ImageField(upload_to='pics/%y/%m/%d/')
    full_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=25)
    address = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    cv = models.FileField(upload_to='documents/%Y/%m/%d')
    upload_date = models.DateTimeField(auto_now_add =True)


    def __str__(self):
        return self.full_name
   

    


   