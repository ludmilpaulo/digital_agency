from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

from .models import ProposalRequest

from information.models import AboutUs

from .serializers import ProposalRequestSerializer

def send_proposal_email(proposal):
    about = AboutUs.objects.first()
    print("Fetched AboutUs:", about)
    context = {
        "title": about.title if about else "Maindo Digital",
        "logo_url": about.logo.url if about and about.logo else "https://www.maindodigital.com/logo.png",
        "email_contact": about.email if about and about.email else "info@maindodigital.com",
        "linkedin": about.linkedin if about and about.linkedin else "",
        "instagram": about.instagram if about and about.instagram else "",
        "facebook": about.facebook if about and about.facebook else "",
        "twitter": about.twitter if about and about.twitter else "",
        "tiktok": about.tiktok if about and about.tiktok else "",
        "github": about.github if about and about.github else "",
        "name": proposal.name,
        "email": proposal.email,
        "phone": proposal.phone,
        "time_frame": proposal.time_frame,
        "company": proposal.company,
        "service": proposal.service,
        "message": proposal.message,
    }
    print("Built context for email:", context)
    html_content = render_to_string("proposal_email_template.html", context)
    print("Rendered HTML content length:", len(html_content))
    return html_content, context  # <-- Now returning both

class ProposalRequestViewSet(viewsets.ModelViewSet):
    queryset = ProposalRequest.objects.all().order_by('-submitted_at')
    
    serializer_class = ProposalRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print("Request data received:", request.data)
        serializer = ProposalRequestSerializer(data=request.data)
        if serializer.is_valid():
            proposal = serializer.save()
            print("Proposal saved:", proposal)
            subject = f"New Proposal Request from {proposal.name}"
            html_content, context = send_proposal_email(proposal)  # <-- Unpack both
            # Email to admin
            print("Sending admin email to:", settings.DEFAULT_FROM_EMAIL)
            msg = EmailMultiAlternatives(
                subject,
                "You have a new proposal request.",
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
            # Email to user
            print("Sending user email to:", proposal.email)
            user_subject = f"Thanks for contacting {context['title']}!"
            user_msg = EmailMultiAlternatives(
                user_subject,
                "Thank you for your request. We'll get in touch soon.",
                settings.DEFAULT_FROM_EMAIL,
                [proposal.email],
            )
            user_msg.attach_alternative(html_content, "text/html")
            user_msg.send(fail_silently=True)
            print("Both emails sent!")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
