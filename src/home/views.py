from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class home_screen_view(View):
    def get(self, request):
        return render(request, 'home/home.html', {})


def error_404(request, exception):
    return render(request, 'error-404.html')
