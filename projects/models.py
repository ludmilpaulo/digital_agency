from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(max_length=200, blank=True)
    badge = models.CharField(max_length=64, blank=True)
    badge_color = models.CharField(max_length=64, blank=True, help_text="e.g. 'bg-yellow-400 text-yellow-900'")
    

    def __str__(self):
        return self.title
    
class ProjectStack(models.Model):
    project = models.ForeignKey(Project, related_name="stack", on_delete=models.CASCADE)
    tech = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.tech} ({self.project.title})"

class ProjectStat(models.Model):
    project = models.ForeignKey(Project, related_name="stats", on_delete=models.CASCADE)
    label = models.CharField(max_length=64)
    value = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.label}: {self.value} ({self.project.title})"

class ProjectCaseStudy(models.Model):
    project = models.OneToOneField(Project, related_name="case_study", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Text', config_name='extends')  # Can use rich text

    def __str__(self):
        return f"{self.title} ({self.project.title})"

class ProjectTrustedBy(models.Model):
    project = models.ForeignKey(Project, related_name="trusted_by", on_delete=models.CASCADE)
    logo = models.ImageField(upload_to="trusted_by/")

    def __str__(self):
        return f"Logo for {self.project.title}"

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