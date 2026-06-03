from django.urls import path

from .views import *

urlpatterns = [

    path(
        'apply/',
        apply_leave,
        name='apply_leave'
    ),

    path(
        'my-leaves/',
        my_leaves,
        name='my_leaves'
    ),


    path(
        'approval/',
        leave_approval_list,
        name='leave_approval_list'
    ),

    path(
        'approve/<int:leave_id>/',
        approve_leave,
        name='approve_leave'
    ),

    path(
        'reject/<int:leave_id>/',
        reject_leave,
        name='reject_leave'
    ),
]