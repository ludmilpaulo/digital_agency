from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import logging
from datetime import datetime
from .models import Appointment
from .serializers import AppointmentSerializer

logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['POST'])
def create_appointment(request):
    logger.debug(f"Received data: {request.data}")

    email = request.data.get('email')
    phone = request.data.get('phone')
    reason = request.data.get('reason')
    date = request.data.get('date')
    time = request.data.get('time')

    if not email or not phone or not reason or not date or not time:
        logger.error("Missing required fields")
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        logger.error("Email already registered")
        return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=email, email=email, password=phone)
        user.save()

        appointment_data = {
            'user': user.id,
            'phone': phone,
            'email': email,
            'date': date,
            'time': time,
            'reason': reason,
        }

        serializer = AppointmentSerializer(data=appointment_data)
        if serializer.is_valid():
            appointment = serializer.save()
            send_appointment_email(appointment, phone)
            return Response({
                "message": "Appointment booked successfully",
                "user_id": user.pk,
                "username": user.username
            }, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error creating appointment: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def send_appointment_email(appointment, password):
    if not appointment.email:
        return

    subject = 'Appointment Confirmation'
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
                    <h1>Appointment Confirmation</h1>
                </div>
                <div class="content">
                    <p>Dear {appointment.user.get_username()},</p>
                    <p>Your appointment is scheduled for <strong>{appointment.date}</strong> at <strong>{appointment.time}</strong>. We are glad to assist you with: <strong>{appointment.reason}</strong>.</p>
                    <p>Your account has been created with the following credentials:</p>
                    <ul>
                        <li>Username: <strong>{appointment.user.get_username()}</strong></li>
                        <li>Password: <strong>{password}</strong></li>
                    </ul>
                    <p>Please feel free to change your password on your profile dashboard.</p>
                    <p>Thank you for choosing our service.</p>
                </div>
                <div class="footer">
                    <p>&copy; {datetime.now().year} Maindo Digital Agency. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [appointment.email]

    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
            html_message=message,
        )
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
