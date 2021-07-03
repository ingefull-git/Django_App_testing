from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from .forms import RegisterUser

def register_view(request):
    form = RegisterUser(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('logchecker:home')
    return render(request, 'register.html', {'form':form})


