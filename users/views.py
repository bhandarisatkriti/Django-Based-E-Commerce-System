from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from  django import forms

from users.forms import SignUpForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in.'.strip())
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'users/login.html')


def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.'.strip())
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully. You can now log in.'.strip())
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.'.strip())
    else:
        form = SignUpForm()

    return render(request, 'users/register.html', {'form': form}) ##{'form': form}-> to pass the form to the template called contex dictinary