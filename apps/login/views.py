from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterUser

def register_view(request):
    form = RegisterUser(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('logchecker:home')
    return render(request, 'register.html', {'form':form})


def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active and user.check_password:
                login(request, user)
                return redirect('logchecker:home')
            else:
                login_errors = 'User or password invalid'
                return render(request, "login.html", {'login_errors': login_errors})
    else:
        if request.user and request.user.is_authenticated:
            return redirect('logchecker:home')
        
    return render(request, "login.html")


def logoutview(request):
    if request.user:
        logout(request)
    return redirect('logchecker:home')

