from django.shortcuts import render

# Create your views here.


def login_show(request):
    return render(request, 'login.html')
