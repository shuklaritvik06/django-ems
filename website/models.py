from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    picture = models.ImageField(default="")
    emp_id = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    age = models.IntegerField()
    address = models.TextField()
    full_time = models.CharField(max_length=3)
    designation = models.CharField(max_length=100)
    salary = models.IntegerField()

    def __str__(self):
        return self.name
