from django.db import models
from employees.models import Employee


class Payroll(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    month = models.IntegerField()

    year = models.IntegerField()

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    present_days = models.IntegerField(
        default=0
    )

    absent_days = models.IntegerField(
        default=0
    )

    deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    generated_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.employee.name}"
            f" - {self.month}/{self.year}"
        )