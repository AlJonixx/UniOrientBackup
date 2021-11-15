from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import random

from customAdmin.forms import AccountAuthenticationForm, DepartmentForm, DesignationForm, EmployeeForm
from .models import *
from django.contrib.auth.hashers import make_password

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

# EMPLOYEE


class all_employee_screen_view(View):
    def get(self, request):
        department = Department.objects.all()
        designation = Designation.objects.all()
        context = {
            'dept': department,
            'desig': designation,
        }
        return render(request, 'admin/employee/employees.html', context)

    def post(self, request):
        form = EmployeeForm(request.POST)
        if request.method == 'POST':
            if 'btnSubmitEmployee' in request.POST:
                empid = random.randint(1000, 9999)
                finalemp = "EMP" + str(empid)
                firstName = request.POST['firstname_text']
                lastName = request.POST['lastname_text']
                userName = request.POST['username_text']
                emailPost = request.POST['email_text']
                passwordPost = request.POST['password_text']
                password2 = request.POST['password2_text']
                joinDate = request.POST['joindate_text']
                phonePost = request.POST['phone_text']
                designationPost = request.POST['designation_text']
                departmentPost = request.POST['department_text']
                hashed_pw = make_password(password2)
                form = Employee(employee_id=finalemp, firstname=firstName, lastname=lastName, username=userName, email=emailPost,
                                password=hashed_pw, phone=phonePost, department=departmentPost, designation=designationPost)
                form.save()
                messages.success(request, "Employee successfully Added!")
                return redirect('all-employee')


def holidays_screen_view(request):
    return render(request, 'admin/employee/holidays.html')


def leaves_admin_screen_view(request):
    return render(request, 'admin/employee/leaves-admin.html')


def leaves_employee_screen_view(request):
    return render(request, 'admin/employee/leaves-employee.html')


def leaves_settings_screen_view(request):
    return render(request, 'admin/employee/leaves-settings.html')


def attendance_admin_screen_view(request):
    return render(request, 'admin/employee/attendance-admin.html')


def attendance_employee_screen_view(request):
    return render(request, 'admin/employee/attendance-employee.html')


class departments_screen_view(View):
    def get(self, request):
        dept = Department.objects.all()
        context = {
            'dept': dept
        }

        return render(request, 'admin/employee/departments.html', context)

    def post(self, request):
        form = DepartmentForm(request.POST)
        if request.method == 'POST':
            if 'btnSubmitDepartment' in request.POST:
                department = request.POST['department_text']
                form = Department(department_name=department)
                form.save()
                messages.success(request, "Deparment successfully Added!")
                return redirect('departments')


class designations_screen_view(View):
    def get(self, request):
        designation = Designation.objects.all()
        department = Department.objects.all()
        context = {
            'desig': designation,
            'dept': department
        }
        return render(request, 'admin/employee/designations.html', context)

    def post(self, request):
        form = DesignationForm(request.POST)
        if request.method == 'POST':
            if 'btnSubmitDesignation' in request.POST:
                designation = request.POST['designation_text']
                department = request.POST['department_text']
                form = Designation(designation_name=designation,
                                   department_name=department)
                form.save()
                messages.success(request, "Designation successfully Added!")
                return redirect('designations')


def timesheet_screen_view(request):
    return render(request, 'admin/employee/timesheet.html')


def shift_scheduling_screen_view(request):
    return render(request, 'admin/employee/shift-scheduling.html')


def overtime_screen_view(request):
    return render(request, 'admin/employee/overtime.html')


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
