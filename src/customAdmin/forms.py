from django import forms
from django.contrib.auth import authenticate
from django.forms import fields, models
from django.forms.widgets import PasswordInput
from customAdmin.models import Department, Designation, Employee, EmployeeAttendance, NewUser


class AccountAuthenticationForm(forms.ModelForm):

    class Meta:
        model = NewUser
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Invalid Login')


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

# class EmployeeAttendaceForm(forms.ModelForm):  # Employee Attendance Form
#     class Meta:
#         model = EmployeeAttendance
#         fields = "__all__"
    
    
