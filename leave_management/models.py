from django.db import models
from employees.models import Employee


class LeaveRequest(models.Model):

    LEAVE_TYPES = (

        ('Casual', 'Casual'),

        ('Sick', 'Sick'),

        ('Paid', 'Paid'),

        ('LOP', 'Loss Of Pay')

    )

    STATUS_CHOICES = (

        ('Pending', 'Pending'),

        ('Approved', 'Approved'),

        ('Rejected', 'Rejected')

    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPES
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.employee.name} - {self.leave_type}"