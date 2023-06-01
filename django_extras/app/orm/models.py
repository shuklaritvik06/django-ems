from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)


class Sellers(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class Books(models.Model):
    publisher = models.OneToOneField(Publisher, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sellers = models.ManyToManyField(Sellers)

# Limit/Offset
#  This can be done using simple slicing
# Order By
# order_by is used in this by passing the string of the field that is to be used for ordering
# Like
# Starts With
# filter(first_name__startswith='')
# Case Insensitivity
# filter(first_name__istartswith='')
# Ends With
# filter(first_name__endswith='')
# Case Insensitivity
# filter(first_name__iendswith='')
# field_name__contains='substring'
# field_name__icontains='substring'
# Range
# Entity.objects.filter(field_name__range=(low_value,high_value))
# Entity.objects.filter(~Q(field_name__range=(low_value,high_value)))
# IS Null
#  Entity.objects.filter(field_name__isnull=True)
# Aggregate (Count, Sum, Min, Max, Average)
# Entity.objects.aggregate(Min(""))
# Exists
# Entity.objects.filter(field_name__isnull=True).exists()
