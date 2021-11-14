"""Admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


from customAdmin.views import (
    admin_screen_view,
    login_screen_view,
    logout_screen_view,
    employee_reports_screen_view,
    payslip_report_screen_view,
    attendance_report_screen_view,
    leave_report_screen_view,
    daily_report_screen_view,
    overtime_report_screen_view,
)


urlpatterns = [
    path('admin-dashboard', admin_screen_view.as_view(), name='admin-dashboard'),
    path('admin-login', login_screen_view, name='admin-login'),
    path('admin-logout', logout_screen_view, name='admin-logout'),
    path('employee-report', employee_reports_screen_view, name='employee-report'),
    path('payslip-report', payslip_report_screen_view, name='payslip-report'),
    path('attendance-report', attendance_report_screen_view,
         name='attendance-report'),
    path('leave-report', leave_report_screen_view, name='leave-report'),
    path('daily-report', daily_report_screen_view, name='daily-report'),
    path('overtime-report', overtime_report_screen_view, name='overtime-report'),
]
