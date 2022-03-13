from datetime import datetime
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
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from django.http import HttpResponse


# Create your views here.


class attendance_screen_view(View):
    def get(self, request):
        emp = Employee.objects.all()
        return render(request, 'take_attendance_template.html', {'empl': emp})

    def post(self, request):
        form = EmployeeAttendance(request.POST)
        if request.method == 'POST':
            if 'TimeLogin' in request.POST:
                empId = request.POST.get("employeeID")
                InOut = request.POST.get("LoginOptions")
                inout = datetime.now().time()
                if InOut == '1':

                    if EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(employee_id_id=empId).exists():
                        if EmployeeAttendance.objects.filter(timeout__isnull=False).filter(todaydate=datetime.today()):
                            messages.success(request, 'Already Timed In!')
                            return redirect('attendance')
                    else:
                        form = EmployeeAttendance(
                            timein=inout, employee_id_id=empId)
                        form.save()
                        messages.success(request, 'Timed In Successfully!')
                        return redirect('attendance')

                else:
                    if EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(employee_id_id=empId).exists():
                        if EmployeeAttendance.objects.filter(timeout__isnull=True).filter(todaydate=datetime.today()):
                            EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(
                                employee_id_id=empId).update(timeout=inout, employee_id_id=empId)
                            messages.success(
                                request, 'Timed Out Successfully!')
                            return redirect('attendance')
                        else:
                            messages.success(request, 'Already Timed Out!')
                            return redirect('attendance')
                    else:
                        messages.success(request, 'You did not Time In!')
                        return redirect('attendance')


class admin_screen_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        totalEmp = Employee.objects.count()
        context = {
            'totalEmp': totalEmp
        }
        return render(request, 'admin/index.html', context)


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


class all_employee_screen_view(LoginRequiredMixin, View):

    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if 'SearchEmp' in request.GET:
            q1 = request.GET['q1']
            q2 = request.GET['q2']
            q3 = request.GET['q3']
            # multiQ = Q(Q(employee_id__icontains=q) & Q(firstname__icontains=q) )

            if q1 and q2 != '':
                employee = Employee.objects.filter(employee_id=q1).filter(
                    Q(firstname=q2) | Q(lastname=q2))
                department = Department.objects.all()
                designation = Designation.objects.all()

            elif q1 and q3 != '':
                employee = Employee.objects.filter(
                    employee_id=q1).filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()

            elif q2 and q3 != '':
                employee = Employee.objects.filter(Q(Q(firstname=q2) | Q(
                    lastname=q2))).filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()

            else:
                if q3 == '':
                    employee = Employee.objects.filter(Q(Q(
                        firstname=q2) | Q(lastname=q2))) or Employee.objects.filter(Q(employee_id=q1))
                else:
                    employee = Employee.objects.filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()
            # print(employee)
            # department = Department.objects.all()
            # designation = Designation.objects.all()
        else:
            department = Department.objects.all()
            designation = Designation.objects.all()
            employee = Employee.objects.all()

        context = {
            'dept': department,
            'desig': designation,
            'empl': employee,
        }

        return render(request, 'admin/employee/employees.html', context)

    def post(self, request):
        form = EmployeeForm(request.POST)
        if request.method == 'POST':
            if 'btnSubmitEmployee' in request.POST:
                default_schedStart = datetime.now().replace(
                    hour=8, minute=0, second=0, microsecond=0)
                default_schedEnd = datetime.now().replace(
                    hour=17, minute=0, second=0, microsecond=0)
                empid = request.POST['employee_id']
                # finalemp = "EMP" + str(empid)
                firstName = request.POST['firstname_text']
                lastName = request.POST['lastname_text']
                userName = request.POST['username_text']
                emailPost = request.POST['email_text']
                # passwordPost = request.POST['password_text']
                # password2 = request.POST['password2_text']
                gender = request.POST['gender_text']
                address = "Edit your Address here"
                phonePost = request.POST['phone_text']
                designationPost = request.POST['designation_text']
                # departmentPost = request.POST['department_text']
                # hashed_pw = make_password(password2)
                form = Employee(employee_id=empid, firstname=firstName, lastname=lastName, username=userName, email=emailPost,
                                phone=phonePost, designation_name_id=designationPost, gender=gender, address=address, sched_start=default_schedStart, sched_end=default_schedEnd)
                form.save()
                messages.success(request, "Employee successfully Added!")
                return redirect('all-employee')

            if 'btnUpdateEmp' in request.POST:
                eid = request.POST.get("emplID")
                fname = request.POST.get("firstname_update")
                lname = request.POST.get("lastname_update")
                uname = request.POST.get("username_update")
                emailUp = request.POST.get("email_update")
                phoneUp = request.POST.get("phone_update")
                # departmentUp = request.POST.get("department_name")
                designationUp = request.POST.get("designation_name")
                # idemp = request.POST.get("empid_update")

                Employee.objects.filter(employee_id=eid).update(firstname=fname, lastname=lname,
                                                       username=uname, email=emailUp, phone=phoneUp, designation_name_id=designationUp)
                messages.success(request, "Employee " +
                                 eid + " successfully Updated!")
                return redirect('all-employee')

    @staticmethod
    def deleteEmp(request, id):
        emp = Employee.objects.get(employee_id=id)
        emp.delete()
        messages.success(request, "Employee successfully Deleted!")
        return redirect('all-employee')


class employee_list_screen_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if 'SearchEmp' in request.GET:
            q1 = request.GET['q1']
            q2 = request.GET['q2']
            q3 = request.GET['q3']
            print(q3)
            # multiQ = Q(Q(employee_id__icontains=q) & Q(firstname__icontains=q) )
            if q1 and q2 != '':
                employee = Employee.objects.filter(employee_id=q1).filter(
                    Q(firstname=q2) | Q(lastname=q2))
                department = Department.objects.all()
                designation = Designation.objects.all()

            elif q1 and q3 != '':
                employee = Employee.objects.filter(
                    employee_id=q1).filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()

            elif q2 and q3 != '':
                employee = Employee.objects.filter(Q(Q(firstname=q2) | Q(
                    lastname=q2))).filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()

            else:
                if q3 == '':
                    employee = Employee.objects.filter(Q(Q(
                        firstname=q2) | Q(lastname=q2))) or Employee.objects.filter(Q(employee_id=q1))
                else:
                    employee = Employee.objects.filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()
            # print(employee)
            # department = Department.objects.all()
            # designation = Designation.objects.all()
        else:
            department = Department.objects.all()
            designation = Designation.objects.all()
            employee = Employee.objects.all()

        context = {
            'dept': department,
            'desig': designation,
            'empl': employee,
        }
        return render(request, 'admin/employee/employees-list.html', context)

    def post(self, request):
        form = EmployeeForm(request.POST)
        if request.method == 'POST':
            if 'btnSubmitEmployee' in request.POST:
                default_schedStart = datetime.now().replace(
                    hour=8, minute=0, second=0, microsecond=0)
                default_schedEnd = datetime.now().replace(
                    hour=17, minute=0, second=0, microsecond=0)
                empid = request.POST['employee_id']
                #finalemp = "EMP" + str(empid)
                firstName = request.POST['firstname_text']
                lastName = request.POST['lastname_text']
                userName = request.POST['username_text']
                emailPost = request.POST['email_text']
                # passwordPost = request.POST['password_text']
                # password2 = request.POST['password2_text']
                gender = request.POST['gender_text']
                address = "Edit your Address here"
                phonePost = request.POST['phone_text']
                designationPost = request.POST['designation_text']
                # departmentPost = request.POST['department_text']
                # hashed_pw = make_password(password2)
                form = Employee(employee_id=empid, firstname=firstName, lastname=lastName, username=userName, email=emailPost,
                                phone=phonePost, designation_name_id=designationPost, gender=gender, address=address, sched_start=default_schedStart, sched_end=default_schedEnd)
                form.save()
                messages.success(request, "Employee successfully Added!")
                return redirect('employee-list')

            if 'btnUpdateEmp' in request.POST:
                eid = request.POST.get("emplID")
                fname = request.POST.get("firstname_update")
                lname = request.POST.get("lastname_update")
                uname = request.POST.get("username_update")
                emailUp = request.POST.get("email_update")
                phoneUp = request.POST.get("phone_update")
                # departmentUp = request.POST.get("department_name")
                designationUp = request.POST.get("designation_name")
                # idemp = request.POST.get("empid_update")

                Employee.objects.filter(employee_id=eid).update(firstname=fname, lastname=lname,
                                                       username=uname, email=emailUp, phone=phoneUp, designation_name_id=designationUp)
                messages.success(request, "Employee " +
                                 eid + " successfully Updated!")
                return redirect('employee-list')


class profile_screen_view(LoginRequiredMixin, View):

    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        employee = Employee.objects.all()
        department = Department.objects.all()
        designation = Designation.objects.all()
        context = {
            'id': id,
            'dept': department,
            'desig': designation,
            'empl': employee,
        }
        return render(request, 'admin/employee/profile.html', context)

    def post(self, request, id):
        if request.method == 'POST':
            if 'btnEditProfile' in request.POST:
                fname = request.POST.get("firstname_profile")
                lname = request.POST.get("lastname_profile")
                # uname = request.POST.get("username_profile")
                # emailProf = request.POST.get("email_update")
                phoneProf = request.POST.get("phone_profile")
                departmentProf = request.POST.get("depart_name")
                designationProf = request.POST.get("desig_name")
                # idempProf = request.POST.get("empid_update")
                gender = request.POST.get("gender")
                address = request.POST.get("address")
                state = request.POST.get("state")
                country = request.POST.get("country")

                Employee.objects.filter(id=id).update(firstname=fname, lastname=lname, phone=phoneProf, department=departmentProf,
                                                      designation=designationProf, gender=gender, address=address, state=state, country=country)
                messages.success(request, "Profile successfully Updated!")
                return redirect('profile', id)


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


class attendance_employee_screen_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if 'btnAttendanceSearch' in request.GET:
            searchDate = request.GET['selectDate']
            searchYear = request.GET['searchYear']
            searchMonth = request.GET['searchMonth']
            emp = Employee.objects.all()
            if searchDate != '':
                date = EmployeeAttendance.objects.filter(todaydate=searchDate)

            elif searchYear != '':
                date = EmployeeAttendance.objects.filter(
                    todaydate__year__gte=searchYear, todaydate__year__lte=searchYear)

            elif searchMonth != '':
                date = EmployeeAttendance.objects.filter(
                    todaydate__month__gte=searchMonth, todaydate__month__lte=searchMonth)

            elif searchYear and searchMonth != '':
                date = EmployeeAttendance.objects.filter(
                    todaydate__year__gte=searchYear, todaydate__month__gte=searchMonth, todaydate__year__lte=searchYear, todaydate__month__lte=searchMonth)

        else:
            emp = Employee.objects.all()
            # empatt = EmployeeAttendance.objects.all()
            today = datetime.today()
            date = EmployeeAttendance.objects.filter(todaydate=today)
            totalMin = EmployeeAttendance.objects.values('timein')

        context = {
            'emp': emp,
            'empatt': date,


        }
        return render(request, 'admin/employee/attendance-employee.html', context)


class departments_screen_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

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

            if 'btnDepartUpdate' in request.POST:
                departID = request.POST.get("deptID")
                departName = request.POST.get("depart_name")

                Department.objects.filter(id=departID).update(
                    department_name=departName)
                messages.success(request, "Deparment successfully Updated!")
                return redirect('departments')

    @staticmethod
    def deleteDepartment(request, id):
        depart = Department.objects.get(id=id)
        depart.delete()
        messages.success(request, "Deparment successfully Deleted!")
        return redirect('departments')


class designations_screen_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

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
                                   department_name_id=department)
                form.save()
                messages.success(request, "Designation successfully Added!")
                return redirect('designations')

            if 'btndesigUpdate' in request.POST:
                desigid = request.POST.get("desigID")
                designame = request.POST.get("desig-name")
                departname = request.POST.get("depart-name")

                Designation.objects.filter(id=desigid).update(
                    designation_name=designame, department_name_id=departname)
                messages.success(request, "Designation successfully Updated!")
                return redirect('designations')

    @staticmethod
    def deleteDesig(request, id):
        desig = Designation.objects.get(id=id)
        desig.delete()
        messages.success(request, "Designation successfully Deleted!")
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


class salary_screen_view(View):
    def get(self, request):
        employee = Employee.objects.all()
        context = {
            'empl': employee,
        }
        return render(request, 'admin/payroll/salary.html', context)

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
