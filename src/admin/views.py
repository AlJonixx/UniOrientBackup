from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class admin_screen_view(View):
    def get(self, request):
        return render(request, 'admin/index.html', {})


class login_screen_view(View):
    def get(self, request):
        return render(request, 'admin/login.html', {})
