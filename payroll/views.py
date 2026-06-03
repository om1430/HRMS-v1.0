from django.shortcuts import render
from datetime import date

from employees.models import Employee
from attendance.models import Attendance

import pandas as pd

from django.http import HttpResponse
from django.shortcuts import render

from employees.models import Employee
from attendance.models import Attendance
from leave_management.models import LeaveRequest


def payroll_dashboard(request):

    employees = Employee.objects.all()

    payroll_data = []

    for employee in employees:

        salary = float(employee.salary)

        present_days = Attendance.objects.filter(
            employee=employee
        ).count()

        approved_leaves = LeaveRequest.objects.filter(
            employee=employee,
            status='Approved'
        ).count()

        total_working_days = 30

        payable_days = (
            present_days +
            approved_leaves
        )

        absent_days = max(
            0,
            total_working_days -
            payable_days
        )

        per_day_salary = (
            salary / total_working_days
        )

        deduction = (
            absent_days *
            per_day_salary
        )

        net_salary = (
            salary - deduction
        )

        payroll_data.append({

            'employee':
                employee.name,

            'salary':
                round(salary, 2),

            'present_days':
                present_days,

            'approved_leaves':
                approved_leaves,

            'absent_days':
                absent_days,

            'deduction':
                round(deduction, 2),

            'net_salary':
                round(net_salary, 2)

        })

    return render(
        request,
        'payroll_dashboard.html',
        {
            'payroll_data':
                payroll_data
        }
    )
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from employees.models import Employee


def generate_payslip(request):

    employee = Employee.objects.get(
        user=request.user
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; '
        'filename="payslip.pdf"'
    )

    p = canvas.Canvas(response)

    p.setFont(
        "Helvetica-Bold",
        18
    )

    p.drawString(
        200,
        800,
        "PAYSLIP"
    )

    p.setFont(
        "Helvetica",
        12
    )

    p.drawString(
        50,
        740,
        f"Employee: {employee.name}"
    )

    p.drawString(
        50,
        710,
        f"Department: {employee.department}"
    )

    p.drawString(
        50,
        680,
        f"Designation: {employee.designation}"
    )

    p.drawString(
        50,
        650,
        f"Basic Salary: ₹{employee.salary}"
    )

    p.drawString(
        50,
        620,
        "Present Days: 28"
    )

    p.drawString(
        50,
        590,
        "Absent Days: 2"
    )

    p.drawString(
        50,
        560,
        "Deduction: ₹4666"
    )

    p.drawString(
        50,
        530,
        "Net Salary: ₹65334"
    )

    p.drawString(
        50,
        470,
        "System Generated Payslip"
    )

    p.showPage()

    p.save()

    return response

def export_payroll_excel(request):

    employees = Employee.objects.all()

    data = []

    for employee in employees:

        salary = float(employee.salary)

        present_days = Attendance.objects.filter(
            employee=employee
        ).count()

        approved_leaves = LeaveRequest.objects.filter(
            employee=employee,
            status='Approved'
        ).count()

        absent_days = max(
            0,
            30 -
            (
                present_days +
                approved_leaves
            )
        )

        deduction = (
            salary / 30
        ) * absent_days

        net_salary = (
            salary -
            deduction
        )

        data.append({

            'Employee':
                employee.name,

            'Salary':
                salary,

            'Present Days':
                present_days,

            'Approved Leaves':
                approved_leaves,

            'Absent Days':
                absent_days,

            'Deduction':
                round(
                    deduction,
                    2
                ),

            'Net Salary':
                round(
                    net_salary,
                    2
                )

        })

    df = pd.DataFrame(data)

    response = HttpResponse(
        content_type=
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; '
        'filename=payroll_report.xlsx'
    )

    df.to_excel(
        response,
        index=False
    )

    return response