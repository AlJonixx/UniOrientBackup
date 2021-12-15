
from datetime import date
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
    sched_start = models.TimeField(blank=True, null=True)
    sched_end = models.TimeField(blank=True, null=True)


# class EmployeeRole(models.Model):
#     employee_id = models.ForeignKey(
#         Employee, on_delete=models.CASCADE)
#     designation_name = models.ForeignKey(
#         Employee, on_delete=models.CASCADE, related_name='emp_designation_name')


class EmployeeAttendance(models.Model): #Employee Attendance Model
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    todaydate = models.DateField(default=date.today)
    timein = models.TimeField(blank=True, null=True)
    timeout = models.TimeField(blank=True, null=True)