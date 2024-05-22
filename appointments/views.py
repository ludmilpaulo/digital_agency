# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime  # Import datetime module
from .models import Appointment
from .serializers import AppointmentSerializer

User = get_user_model()

class AppointmentCreateAPIView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        try:
            username = self.request.data.get('email')
            phone = self.request.data.get('phone')
            email = self.request.data.get('email')
            password = self.request.data.get('phone')

            print("Validating inputs...")
            if not username or not email or not password:
                print("Validation error: Missing fields")
                raise ValidationError({"error": "All fields are required"}, code=400)

            print("Checking for existing username and email...")
            if User.objects.filter(username=username).exists():
                print("Validation error: Username exists")
                raise ValidationError({"error": "Username already exists"}, code=400)
            if User.objects.filter(email=email).exists():
                print("Validation error: Email registered")
                raise ValidationError({"error": "Email already registered"}, code=400)

            print("Creating user...")
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            print("User created successfully")

            appointment = serializer.save(user=user)
            print(f"Appointment saved: {appointment}")

            print("Sending email...")
            self.send_appointment_email(appointment, password)

            print("Signup successful")
            return Response({
                "message": "Signup successful",
                "user_id": user.pk,
                "username": user.username
            }, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            print("Validation error:", str(ve))
            raise ve

        except Exception as e:
            print("Unexpected error:", str(e))
            raise ValidationError({"error": str(e)}, code=400)

    def send_appointment_email(self, appointment, password):
        if not appointment.email:
            print("No email provided, skipping email sending")
            return  # If no email provided in the appointment, do not attempt to send an email

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
                html_message=message,  # Add this parameter to send HTML email
            )
            print("Appointment email sent")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
