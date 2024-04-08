from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    picture = models.ImageField(default="default.jpg")
    emp_id = models.PositiveIntegerField(primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    address = models.TextField()
    FULL_TIME_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]
    full_time = models.CharField(max_length=3, choices=FULL_TIME_CHOICES)
    designation = models.CharField(max_length=100)
    salary = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
