# Generated by Django 4.1.7 on 2023-05-29 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0003_employee_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="full_time",
            field=models.CharField(max_length=3),
        ),
    ]
