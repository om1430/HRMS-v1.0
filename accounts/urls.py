from django.urls import path
from .views import *

urlpatterns = [

    path(
        '',
        login_view,
        name='login'
    ),

    path(
        'admin-dashboard/',
        admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'employee-dashboard/',
        employee_dashboard,
        name='employee_dashboard'
    ),

    path(
        'profile/',
        employee_profile,
        name='employee_profile'
    ),

    path(
        'attendance-history/',
        attendance_history,
        name='attendance_history'
    ),
]