from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Attendance
from employees.models import Employee


def attendance_list(request):

    attendance_records = Attendance.objects.all()

    return render(
        request,
        'attendance_list.html',
        {
            'attendance_records': attendance_records
        }
    )


def attendance_action(request):

    if request.method == 'POST':

        employee = Employee.objects.first()

        today = timezone.now().date()

        action = request.POST.get('action')

        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today
        )

        if action == 'checkin':
            attendance.check_in = timezone.now()

        elif action == 'checkout':
            attendance.check_out = timezone.now()

        attendance.save()

        return redirect('/attendance/action/')

    return render(
        request,
        'attendance_action.html'
    )