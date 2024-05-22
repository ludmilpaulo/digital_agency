from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from datetime import datetime 
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
        message = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f4f4f4;
                    }}
                    .email-container {{
                        max-width: 600px;
                        margin: auto;
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{
                        background-color: #4CAF50;
                        padding: 10px;
                        text-align: center;
                        color: white;
                        border-top-left-radius: 10px;
                        border-top-right-radius: 10px;
                    }}
                    .content {{
                        padding: 20px;
                    }}
                    .content p {{
                        line-height: 1.6;
                    }}
                    .footer {{
                        margin-top: 20px;
                        text-align: center;
                        font-size: 12px;
                        color: #888888;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="header">
                        <h1>Application Received</h1>
                    </div>
                    <div class="content">
                        <p>Dear {self.full_name},</p>
                        <p>Thank you for applying to join our team at Maindo Digital Agency! We have received your application for the position of <strong>{self.career.title}</strong> and will review your qualifications and experience thoroughly.</p>
                        <p>Please allow us a week to process your application. If you do not hear from us within two weeks, it does not mean the journey ends here! We are always on the lookout for talented individuals and will keep your application on file for future opportunities that match your skills and passion.</p>
                        <p>We appreciate your interest in joining our team and wish you the best of luck with your application.</p>
                        <p>Warm regards,<br>Maindo Digital Agency Team</p>
                    </div>
                    <div class="footer">
                        <p>&copy; {datetime.now().year} Maindo Digital Agency. All rights reserved.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        send_mail(subject, "", from_email, [self.email], fail_silently=False, html_message=message)
