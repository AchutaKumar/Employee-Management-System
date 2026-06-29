from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('',views.employee_list, name='employee_list'),
    path('employee/<int:pk>/',views.employee_detail, name='employee_detail'),
    path('employee/create/',views.employee_create, name='employee_create'),
    path('employee/update/<int:pk>/',views.employee_update, name='employee_update'),
    path('employee/delete/<int:pk>/',views.employee_delete, name='employee_delete'),
]