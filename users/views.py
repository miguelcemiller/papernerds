from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout

from . forms import LoginForm
from django.contrib.auth.models import User


def landingView(request):
    return render(request, 'users/landing.html')


def loginView(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("logged in")
        else:
            print('Username or password is incorrect')

    return render(request, 'users/login.html')

def logoutView(request):
    logout(request)
    return redirect('login')


# def homeView(request):
#     return render(request, 'papers/home.html')
