from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=64, blank=True)  # e.g. 'fa-code'
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Plan(models.Model):
    service = models.ForeignKey(Service, related_name="plans", on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    price = models.CharField(max_length=32)
    features = models.JSONField(default=list, blank=True)
    cta = models.CharField(max_length=32, default="Get Started")
    popular = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.service.title})"
    
    
class ProposalRequest(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=80, blank=True)
    service = models.CharField(max_length=100, blank=True)
    time_frame = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"