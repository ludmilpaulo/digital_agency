# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentCreateAPIView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        phone = self.request.data.get('phone')
        
        if not email or not phone:
            return Response({"error": "Email and phone number are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user, created = User.objects.get_or_create(username=email, defaults={'email': email})
            if created:
                user.set_password(phone)
                user.save()
            else:
                return Response({"error": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        appointment = serializer.save(user=user)
        self.send_appointment_email(appointment, phone)

    def send_appointment_email(self, appointment, password):
        if not appointment.email:
            return  # If no email provided in the appointment, do not attempt to send an email

        subject = 'Appointment Confirmation'
        message = (
            f"Dear {appointment.user.get_username()},\n\n"
            f"Your appointment is scheduled for {appointment.date} at {appointment.time}. "
            f"We are glad to assist you with: {appointment.reason}.\n\n"
            f"Your account has been created with the following credentials:\n"
            f"Username: {appointment.user.get_username()}\n"
            f"Password: {password}\n\n"
            f"Please feel free to change your password on your profile dashboard.\n\n"
            "Thank you for choosing our service."
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [appointment.email]

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
