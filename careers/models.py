from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from django.core.mail import send_mail

class Career(models.Model):
    title = models.CharField(max_length=100)
    description = CKEditor5Field('Text', config_name='extends')

    def __str__(self):
        return self.title



class JobApplication(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"Application for {self.career.title} by {self.full_name}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new application
        super(JobApplication, self).save(*args, **kwargs)
        if is_new:
            self.send_confirmation_email()

    def send_confirmation_email(self):
        subject = f"Application Received for {self.career.title}"
        from_email = settings.DEFAULT_FROM_EMAIL
        message = (
            f"Dear {self.full_name},\n\n"
            "Thank you for applying to join our team at Maindo Digital Agency! "
            "We have received your application for the position of "
            f"{self.career.title} and will review your qualifications and experience thoroughly.\n\n"
            "Please allow us a week to process your application. "
            "If you do not hear from us within two weeks, it does not mean the journey ends here! "
            "We are always on the lookout for talented individuals and will keep your application on file "
            "for future opportunities that match your skills and passion.\n\n"
            "We appreciate your interest in joining our team and wish you the best of luck with your application.\n\n"
            "Warm regards,\n"
            "Maindo Digital Agency Team"
        )
        send_mail(subject, message, from_email, [self.email], fail_silently=False)
