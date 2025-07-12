from django.db import models

from django_ckeditor_5.fields import CKEditor5Field

from django.contrib.auth import get_user_model
User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='authors/', blank=True, null=True)
    bio = models.TextField(blank=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.name() or self.user.username

class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS = (('draft', 'Draft'), ('published', 'Published'), ('scheduled', 'Scheduled'))
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Text', config_name='extends')
    markdown = models.TextField(blank=True)  # Optional: keep the markdown too
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    published_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS, default='draft')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    newsletter_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=True)

    def __str__(self):
        return self.email
