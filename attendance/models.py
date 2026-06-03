from django.db import models
from employees.models import Employee


class Attendance(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    check_in = models.DateTimeField(
        null=True,
        blank=True
    )

    check_out = models.DateTimeField(
        null=True,
        blank=True
    )

    latitude = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    longitude = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    selfie = models.ImageField(
        upload_to='attendance_selfies/',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default='Present'
    )

    def __str__(self):

        return f"{self.employee.name} - {self.date}"