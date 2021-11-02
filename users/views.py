from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from urllib.parse import urlparse

from django.contrib.auth.models import User


def landingView(request):
    return render(request, 'users/landing.html')


def loginView(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            print("Username does not exist")

        user = authenticate(request, username=username, password=password)

        # Get current path
        current_path = urlparse(request.META.get('HTTP_REFERER')).path

        if user is not None:
            login(request, user)
            print("logged in")

            # If full path is 127.0.0.1:8000/login, redirect to home
            if current_path == '/login/':
                return redirect('home')
            else: # Else stay on current path
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        else:
            print('Username or password is incorrect')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
           
    #return render(request, 'papers/paper.html', context_instance=RequestContext(request))
    #return redirect(request.path)
    return render(request, 'users/login.html')
    

def logoutView(request):
    logout(request)
    return redirect('landing')



# def homeView(request):
#     return render(request, 'papers/home.html')
