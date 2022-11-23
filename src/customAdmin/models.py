
from datetime import date
from operator import truediv
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name

class AccountOfficer(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=150, blank=True)
    confirm_password = models.CharField(max_length=150, blank=True)

class Department(models.Model):  # Deparment Model
    department_name = models.CharField(max_length=150, unique=True)


class Designation(models.Model):  # Designation MOdel
    designation_name = models.CharField(max_length=150, unique=True)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)


class Employee(models.Model):  # Employee Model
    employee_id = models.BigAutoField(primary_key=True, unique=True)
    firstname = models.CharField(max_length=150, blank=True)
    lastname = models.CharField(max_length=150, blank=True)
    username = models.CharField(max_length=150, blank=True, unique=True)
    email = models.EmailField(_('email address'), unique=True, blank=True)
    # password = models.CharField(max_length=150, blank=True)
    join_date = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length=150, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    designation_name = models.ForeignKey(
        Designation, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    birthDate = models.DateField(blank=True, null=True)
    passNo = models.CharField(max_length=150, blank=True)
    passExp = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    maritalStatus = models.CharField(max_length=20, blank=True)
    children = models.CharField(max_length=20, blank=True)
    sched_start = models.TimeField(blank=True, null=True)
    sched_end = models.TimeField(blank=True, null=True)


# class EmployeeRole(models.Model):
#     employee_id = models.ForeignKey(
#         Employee, on_delete=models.CASCADE)
#     designation_name = models.ForeignKey(
#         Employee, on_delete=models.CASCADE, related_name='emp_designation_name')

class PrimaryEmergencyContacts(models.Model):
    employee_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150, blank=True)
    relationship = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)


class EmployeeAttendance(models.Model):  # Employee Attendance Model
    employee_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True)
    todaydate = models.DateField(default=date.today)
    timein = models.TimeField(blank=True, null=True)
    timeout = models.TimeField(blank=True, null=True)
    hours = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=150, blank=True, null=True)
    remarks = models.CharField(max_length=150, blank=True, null=True)
    lateMin = models.IntegerField(blank=True, null=True)


class EmployeeSalary(models.Model):  # Employee Salary Model
    employee_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True)
    base_salary = models.IntegerField(blank=True, null=True)
    daily_rate = models.IntegerField(blank=True, null=True)
    gross_salary = models.IntegerField(blank=True, null=True)
    sss = models.IntegerField(blank=True, null=True)
    pag_ibig = models.IntegerField(blank=True, null=True)
    philhealth = models.IntegerField(blank=True, null=True)
    net_salary = models.IntegerField(blank=True, null=True)


class EmployeeSchedule(models.Model):
    timein = models.TimeField(blank=True, null=True)
    timeout = models.TimeField(blank=True, null=True)
    status = models.CharField(
        max_length=150, blank=True, null=True, default="INACTIVE")
