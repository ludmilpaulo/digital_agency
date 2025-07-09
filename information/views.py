from rest_framework import generics
from rest_framework import viewsets
from .models import Image, Carousel, AboutUs, Partner, Timeline, Why_Choose_Us, Team, Contact
from .serializers import ImageSerializer, CarouselSerializer, AboutUsSerializer, PartnerSerializer, TimelineSerializer, WhyChooseUsSerializer, TeamSerializer, ContactSerializer

# ListCreateAPIView for creating and listing all instances
class ImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class CarouselListCreateAPIView(generics.ListCreateAPIView):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer

class AboutUsListCreateAPIView(generics.ListCreateAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

class WhyChooseUsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Why_Choose_Us.objects.all()
    serializer_class = WhyChooseUsSerializer

class TeamListCreateAPIView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

# RetrieveUpdateDestroyAPIView for retrieving, updating and deleting a single instance
class ImageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class CarouselRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer

class AboutUsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

class WhyChooseUsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Why_Choose_Us.objects.all()
    serializer_class = WhyChooseUsSerializer

class TeamRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class ContactRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    
class TimelineListAPIView(generics.ListAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer

class PartnerListAPIView(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    
    
# information/views.py
from rest_framework import generics
from .models import Contact
from .serializers import ContactSerializer
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class ContactListCreateAPIView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        contact = serializer.save()
        self.send_notification_emails(contact)

    def send_notification_emails(self, contact):
        # Send to Admin
        subject_admin = f"New Contact Message: {contact.subject}"
        html_content_admin = f"""
        <div style="font-family:Arial,sans-serif;background:#f7f8fc;padding:30px;">
          <div style="max-width:600px;margin:auto;background:#fff;padding:30px;border-radius:12px;border:1px solid #ececec;">
            <h2 style="color:#2b308b;margin-bottom:18px;">📥 New Contact Message</h2>
            <p><b>Subject:</b> {contact.subject}</p>
            <p><b>From:</b> {contact.from_email} | <b>Phone:</b> {contact.phone}</p>
            <p><b>Message:</b></p>
            <p style="background:#f1f3f8;border-radius:8px;padding:18px 20px;color:#333;">{contact.message}</p>
          </div>
        </div>
        """
        msg_admin = EmailMultiAlternatives(
            subject_admin,
            html_content_admin,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],  # send to your admin email
        )
        msg_admin.attach_alternative(html_content_admin, "text/html")
        msg_admin.send()

        # Send to User
        subject_user = "Thank you for contacting Maindo Digital Agency"
        html_content_user = f"""
        <div style="font-family:Arial,sans-serif;background:#f5f8fe;padding:36px;">
          <div style="max-width:580px;margin:auto;background:#fff;padding:30px 26px;border-radius:12px;border:1px solid #ececec;">
            <div style="text-align:center">
              <img src="https://www.maindodigital.com/logo.png" alt="Maindo Logo" width="64" style="margin-bottom:18px;">
            </div>
            <h2 style="color:#2b308b;margin-bottom:10px;text-align:center;">Thank you for reaching out! 👋</h2>
            <p>Hi <b>{contact.from_email}</b>,</p>
            <p>We’ve received your message and will get back to you as soon as possible (usually within 2 hours during business hours).</p>
            <div style="background:#f2f5fb;border-radius:8px;padding:18px 20px;color:#555;margin:24px 0;">
                <b>Your Message:</b><br>
                <span style="color:#222;">{contact.message}</span>
            </div>
            <p>Need urgent help? WhatsApp us at <b>{contact.phone}</b> or reply to this email.</p>
            <p style="margin-top:34px;">Best regards,<br><b>Maindo Digital Agency Team</b></p>
            <hr style="margin:32px 0 20px 0;border:none;border-bottom:1px solid #ececec;">
            <div style="font-size:13px;text-align:center;color:#a0a0a0;">
              <a href="https://www.maindodigital.com" style="color:#2b308b;text-decoration:none;">www.maindodigital.com</a>
            </div>
          </div>
        </div>
        """
        msg_user = EmailMultiAlternatives(
            subject_user,
            html_content_user,
            settings.DEFAULT_FROM_EMAIL,
            [contact.from_email],
        )
        msg_user.attach_alternative(html_content_user, "text/html")
        msg_user.send()
