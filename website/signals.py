import os

from django.contrib.auth.models import Group
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Employee
import smtplib


s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(user="ritvikshukla261@gmail.com", password=os.getenv("password"))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        group, ok = Group.objects.get_or_create(name="employee")
        group.user_set.add(instance)
        s.sendmail("ritvikshukla261@gmail.com", instance.email, f"Subject: Welcome to ABC Company!\n\nYou are added "
                                                                f"to the organization \n\n Your"
                                                                f"login credentials are\n\nusername={instance.username}"
                                                                f"\n" f"password=ems"
                                                                f"{instance.username}{instance.first_name}")
    else:
        s.sendmail("ritvikshukla261@gmail.com", instance.email, f"Subject: Your info have been updated\n\n"
                                                                f"Hey {instance.first_name} {instance.last_name} Your"
                                                                f"information have been updated on the"
                                                                f"portal")


@receiver(post_delete, sender=Employee)
def delete_user(sender, instance, **kwargs):
    s.sendmail("ritvikshukla261@gmail.com", instance.email, f"Subject: You have been removed from the ABC!\n\n"
                                                            f"Hey {instance.user.first_name} {instance.user.last_name} You have"
                                                            f" been removed from the company ABC")
