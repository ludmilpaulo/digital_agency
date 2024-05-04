# views.py
from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentCreateAPIView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        appointment = serializer.save()
        self.send_appointment_email(appointment)

    def send_appointment_email(self, appointment):
        if not appointment.email:
            return  # If no email provided in the appointment, do not attempt to send an email

        subject = 'Appointment Confirmation'
        message = (
            f"Dear {appointment.user.get_username()},\n\n"
            f"Your appointment is scheduled for {appointment.date} at {appointment.time}. "
            f"We are glad to assist you with: {appointment.reason}.\n\n"
            "Thank you for choosing our service."
        )
        from_email = settings.DEFAULT_FROM_EMAIL  # Your own email for the 'From' header
        recipient_list = [appointment.email]  # The email provided in the POST request

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
