from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    employee_code = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    designation = models.CharField(
        max_length=100
    )

    department = models.CharField(
        max_length=100
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    joining_date = models.DateField()

    status = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name    


leave_balance = models.IntegerField(
    default=12
)

address = models.TextField(
    blank=True,
    null=True
)

emergency_contact = models.CharField(
    max_length=20,
    blank=True,
    null=True
)

photo = models.ImageField(
    upload_to='employees/',
    blank=True,
    null=True
)