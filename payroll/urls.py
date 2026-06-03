from django.urls import path
from .views import *

urlpatterns = [

    path(
        '',
        payroll_dashboard,
        name='payroll_dashboard'
    ),

    path(
        'payslip/',
        generate_payslip,
        name='generate_payslip'
    ),

    path(
        'export/',
        export_payroll_excel,
        name='export_payroll_excel'
    ),
]