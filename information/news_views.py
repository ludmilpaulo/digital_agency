# information/views.py

import secrets
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
from rest_framework import generics, status
from rest_framework.response import Response
from .models import NewsletterSubscriber
from .serializers import NewsletterSubscriberSerializer

class NewsletterSubscribeAPIView(generics.CreateAPIView):
    serializer_class = NewsletterSubscriberSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "").strip().lower()
        if not email:
            return Response({"email": "Email is required."}, status=400)
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if subscriber.is_confirmed:
            return Response({"detail": "You are already subscribed!"}, status=400)
        # (Re)send confirmation
        token = secrets.token_urlsafe(32)
        subscriber.confirm_token = token
        subscriber.is_confirmed = False
        subscriber.save()
        confirm_url = f"{settings.FRONTEND_URL}/newsletter/confirm/{token}/"
        html_content = render_to_string(
            "information/newsletter_confirm.html", {"confirm_url": confirm_url}
        )
        subject = "Confirm your subscription - Maindo Digital Agency"
        email_msg = EmailMultiAlternatives(subject, html_content, settings.DEFAULT_FROM_EMAIL, [email])
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()
        return Response(
            {"detail": "Confirmation email sent! Please check your inbox."},
            status=status.HTTP_201_CREATED if created else 200,
        )

class NewsletterConfirmAPIView(generics.GenericAPIView):
    def get(self, request, token):
        try:
            subscriber = NewsletterSubscriber.objects.get(confirm_token=token)
        except NewsletterSubscriber.DoesNotExist:
            return Response({"detail": "Invalid or expired confirmation link."}, status=400)
        subscriber.is_confirmed = True
        subscriber.confirm_token = None
        subscriber.save()
        return Response({"detail": "Your email is now confirmed and you're subscribed! 🎉"})
