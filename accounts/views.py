from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from employees.models import Employee
from attendance.models import Attendance

import base64
from django.core.files.base import ContentFile


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_superuser:

                return redirect(
                    'admin_dashboard'
                )

            else:

                return redirect(
                    'employee_dashboard'
                )

        return render(
            request,
            'login.html',
            {
                'error': 'Invalid Username or Password'
            }
        )

    return render(
        request,
        'login.html'
    )


@login_required
def admin_dashboard(request):

    from attendance.models import Attendance

    try:

        from leave_management.models import LeaveRequest

        pending_leaves = LeaveRequest.objects.filter(
            status='Pending'
        ).count()

    except:

        pending_leaves = 0

    total_employees = Employee.objects.count()

    present_today = Attendance.objects.filter(
        date=timezone.now().date()
    ).count()

    context = {

        'total_employees': total_employees,

        'present_today': present_today,

        'pending_leaves': pending_leaves

    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )


@login_required
def employee_dashboard(request):

    employee = Employee.objects.get(
        user=request.user
    )

    today = timezone.now().date()

    attendance, created = Attendance.objects.get_or_create(
        employee=employee,
        date=today
    )

    if request.method == 'POST':

        action = request.POST.get('action')

        latitude = request.POST.get('latitude')

        longitude = request.POST.get('longitude')

        selfie = request.FILES.get('selfie')

        selfie_data = request.POST.get(
            'selfie_data'
        )

        if action == 'checkin':

            if not attendance.check_in:

                attendance.check_in = timezone.now()

            attendance.latitude = latitude

            attendance.longitude = longitude

            # Mobile Camera Upload
            if selfie:

                attendance.selfie = selfie

            # Laptop Webcam Capture
            elif selfie_data:

                try:

                    format, imgstr = selfie_data.split(
                        ';base64,'
                    )

                    ext = format.split('/')[-1]

                    file_name = (
                        f"{employee.id}_{today}.{ext}"
                    )

                    attendance.selfie.save(
                        file_name,
                        ContentFile(
                            base64.b64decode(imgstr)
                        ),
                        save=False
                    )

                except Exception as e:

                    print(
                        "Selfie Error:",
                        e
                    )

        elif action == 'checkout':

            if attendance.check_in and not attendance.check_out:

                attendance.check_out = timezone.now()

        attendance.save()

    status = "Not Marked"

    if attendance.check_in:
        status = "Checked In"

    if attendance.check_out:
        status = "Checked Out"

    context = {

        'employee_name': employee.name,

        'status': status,

        'attendance': attendance

    }

    return render(
        request,
        'employee_dashboard.html',
        context
    )

@login_required
def employee_profile(request):

    employee = Employee.objects.get(
        user=request.user
    )

    return render(
        request,
        'employee_profile.html',
        {
            'employee': employee
        }
    )

@login_required
def attendance_history(request):

    employee = Employee.objects.get(
        user=request.user
    )

    records = Attendance.objects.filter(
        employee=employee
    ).order_by(
        '-date'
    )

    return render(
        request,
        'attendance_history.html',
        {
            'records': records
        }
    )