from django.urls import path
from .views import attendance_list
from .views import attendance_action

urlpatterns = [

    path(
        '',
        attendance_list,
        name='attendance_list'
    ),

    path(
        'action/',
        attendance_action,
        name='attendance_action'
    ),
]