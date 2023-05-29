from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    emp_id = models.IntegerField()
    email = models.EmailField()
    phone = models.IntegerField()
    age = models.IntegerField()
    address = models.TextField()
    full_time = models.BooleanField()
    designation = models.CharField(max_length=100)
    salary = models.IntegerField()

    def __str__(self):
        return self.name
