from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
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
