from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(to_email):
    subject = "Welcome to Airport System"
    message = "Hello! Thank you for registering in our system."
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject,
        message,
        from_email,
        [to_email],
        fail_silently=False,
    )
    return f"Email sent to {to_email}"