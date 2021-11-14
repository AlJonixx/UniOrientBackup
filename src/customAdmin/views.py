from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from customAdmin.forms import AccountAuthenticationForm
from .models import *

from django.http import HttpResponse


# Create your views here.


class admin_screen_view(View):
    def get(self, request):
        return render(request, 'admin/index.html', {})


def logout_screen_view(request):
    logout(request)
    return redirect('admin-login')


# AUTHENTICATION

def login_screen_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('admin-dashboard')

    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('admin-dashboard') 
                
        else:
            messages.info(request, 'Email or Password do not match!')
            return redirect('admin-login')
    else:
        form = AccountAuthenticationForm()

    context['form'] = form
    return render(request, 'admin/login.html', context)

# END AUTHENTICATION

# START PAYROLL


def payroll_items_screen_view(request):
    return render(request, 'admin/payroll/payroll-items.html')


def salary_view_screen_view(request):
    return render(request, 'admin/payroll/salary-view.html')


def salary_screen_view(request):
    return render(request, 'admin/payroll/salary.html')

# END PAYROLL

# START OF REPORT VIEWS


def employee_reports_screen_view(request):
    return render(request, 'admin/reports/employee_reports.html', {})


def payslip_report_screen_view(request):
    return render(request, 'admin/reports/payslip_report.html', {})


def attendance_report_screen_view(request):
    return render(request, 'admin/reports/attendance_report.html', {})


def leave_report_screen_view(request):
    return render(request, 'admin/reports/leave_report.html', {})


def daily_report_screen_view(request):
    return render(request, 'admin/reports/daily_report.html', {})


def overtime_report_screen_view(request):
    return render(request, 'admin/reports/overtime_report.html', {})

# END OF REPORT VIEWS
