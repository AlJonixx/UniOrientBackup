from django import forms
from django.contrib.auth import authenticate
from django.forms import fields, models
from django.forms.widgets import PasswordInput
<<<<<<< HEAD
from customAdmin.models import Department, Designation, Employee, EmployeeAttendance, EmployeeSalary, NewUser, PrimaryEmergencyContacts, AccountOfficer
from django.contrib.auth.forms import UserCreationForm
=======
from customAdmin.models import Department, Designation, Employee, EmployeeAttendance, EmployeeSchedule, EmployeeSalary, NewUser, PrimaryEmergencyContacts

from customAdmin.models import *
>>>>>>> 70f4444c3cd36f19ef711b45d9d0106f53ccc2f1


class AccountAuthenticationForm(forms.ModelForm):

    class Meta:
        model = NewUser
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Invalid Login')

<<<<<<< HEAD
class AccountForm(UserCreationForm):

=======

class AccountOfficerForm(forms.ModelForm):  # Account Officer
>>>>>>> 70f4444c3cd36f19ef711b45d9d0106f53ccc2f1
    class Meta:
        model = NewUser
        fields = ['user_name','email', 'password']

class AccountOfficerForm(forms.ModelForm): # Account Officer
   class Meta:
        model = AccountOfficer
        fields = "__all__"


class DepartmentForm(forms.ModelForm):  # Department Form
    class Meta:
        model = Department
        fields = "__all__"


class DesignationForm(forms.ModelForm):  # Designation Form
    class Meta:
        model = Designation
        fields = "__all__"


class EmployeeForm(forms.ModelForm):  # Employee Form
    class Meta:
        model = Employee
        fields = "__all__"


class EmergencyContactForm(forms.ModelForm):  # Emergency Contact Form
    class Meta:
        model = PrimaryEmergencyContacts
        fields = "__all__"


class EmployeeSalaryForm(forms.ModelForm):
    class Meta:
        model = EmployeeSalary
        fields = "__all__"


class EmployeSchduleForm(forms.ModelForm):
    class Meta:
        model = EmployeeSchedule
        fields = "__all__"

# class EmployeeAttendaceForm(forms.ModelForm):  # Employee Attendance Form
#     class Meta:
#         model = EmployeeAttendance
#         fields = "__all__"
