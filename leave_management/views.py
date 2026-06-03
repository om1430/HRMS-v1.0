from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from employees.models import Employee
from .models import LeaveRequest
from django.shortcuts import get_object_or_404

@login_required
def apply_leave(request):

    employee = Employee.objects.get(
        user=request.user
    )

    if request.method == 'POST':

        LeaveRequest.objects.create(

            employee=employee,

            leave_type=request.POST.get(
                'leave_type'
            ),

            start_date=request.POST.get(
                'start_date'
            ),

            end_date=request.POST.get(
                'end_date'
            ),

            reason=request.POST.get(
                'reason'
            )

        )

        return redirect(
            'my_leaves'
        )

    return render(
        request,
        'apply_leave.html'
    )


@login_required
def my_leaves(request):

    employee = Employee.objects.get(
        user=request.user
    )

    leaves = LeaveRequest.objects.filter(
        employee=employee
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'my_leaves.html',
        {
            'leaves': leaves
        }
    )

@login_required
def leave_approval_list(request):

    leaves = LeaveRequest.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'leave_approval_list.html',
        {
            'leaves': leaves
        }
    )


@login_required
def approve_leave(request, leave_id):

    leave = get_object_or_404(
        LeaveRequest,
        id=leave_id
    )

    if leave.status == 'Pending':

        leave.status = 'Approved'

        leave.save()

        employee = leave.employee

        employee.leave_balance -= 1

        if employee.leave_balance < 0:
            employee.leave_balance = 0

        employee.save()

    return redirect(
        'leave_approval_list'
    )


@login_required
def reject_leave(request, leave_id):

    leave = get_object_or_404(
        LeaveRequest,
        id=leave_id
    )

    leave.status = 'Rejected'

    leave.save()

    return redirect(
        'leave_approval_list'
    )