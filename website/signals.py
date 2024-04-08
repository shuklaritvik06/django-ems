import os
import smtplib

from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from . import models

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

try:
    EMAIL_USER = os.getenv("MY_EMAIL")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    if not EMAIL_USER or not EMAIL_PASSWORD:
        raise ValueError("Email credentials are not provided")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

try:
    smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp_server.starttls()
    res = smtp_server.login(user=EMAIL_USER, password=EMAIL_PASSWORD)
    if res:
        print("Connected to SMTP")
except Exception as e:
    print(f"SMTP connection error: {e}")
    exit(1)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            group, created = Group.objects.get_or_create(name="employee")
            group.user_set.add(instance)
            subject = "Welcome to ABC Company!"
            print(instance.email)
            message = (
                f"Subject: {subject}\n\n"
                f"You have been added to the organization.\n\n"
                f"Your login credentials are:\n\n"
                f"Username: {instance.username}\n"
                f"Password: ems{instance.username}{instance.first_name}"
            )
            smtp_server.sendmail(EMAIL_USER, instance.email, message)
        except Exception as e:
            print(f"Error sending welcome email: {e}")


@receiver(post_delete, sender=models.Employee)
def delete_user(sender, instance, **kwargs):
    try:
        subject = "You have been removed from ABC!"
        print(instance.email)
        message = (
            f"Subject: {subject}\n\n"
            f"Hey {instance.user.first_name} {instance.user.last_name},\n\n"
            f"You have been removed from the company ABC."
        )
        smtp_server.sendmail(EMAIL_USER, instance.email, message)
    except Exception as e:
        print(f"Error sending deletion email: {e}")

