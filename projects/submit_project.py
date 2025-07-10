from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .serializers import ProjectInquirySerializer

ADMIN_EMAILS = ["support@maindodigital.com"]  # <-- Replace with your real admin email(s)


def send_admin_notification(data):
    subject = f"🚀 New Project Inquiry from {data['name']}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_emails = ADMIN_EMAILS

    html_content = render_to_string(
        "emails/project_inquiry.html",  # Path to admin HTML template
        data
    )
    text_content = (
        f"New Project Inquiry\n\n"
        f"Name: {data['name']}\n"
        f"Email: {data['email']}\n"
        f"Phone: {data['phone']}\n"
        f"Company: {data['company']}\n"
        f"Project: {data['project']}\n"
        f"Budget: {data['budget']}\n"
        f"Message:\n{data['message']}\n"
    )

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_user_confirmation(data):
    subject = "We've received your project brief! 🚀 | Maindo Digital"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_emails = [data['email']]

    html_content = render_to_string(
        "emails/project_inquiry_user.html",  # Path to user HTML template
        data
    )
    text_content = (
        f"Thank you, {data['name']}!\n\n"
        f"We have received your project inquiry. Our team at Maindo Digital will get in touch soon.\n\n"
        f"Project: {data['project']}\n"
        f"Budget: {data['budget']}\n"
        f"Message: {data['message']}\n"
        f"Visit us: www.maindodigital.com"
    )

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@api_view(["POST"])
@permission_classes([AllowAny])
def submit_project_inquiry(request):
    serializer = ProjectInquirySerializer(data=request.data)
    if serializer.is_valid():
        inquiry = serializer.save()
        # Send notification to admin
        try:
            send_admin_notification(serializer.data)
        except Exception as e:
            print("Failed to send admin notification email:", e)
        # Send confirmation to user
        try:
            send_user_confirmation(serializer.data)
        except Exception as e:
            print("Failed to send confirmation to user:", e)
        return Response({"detail": "Submission received."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
