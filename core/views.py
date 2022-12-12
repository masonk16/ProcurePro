from django.shortcuts import render


from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .forms import *


def register(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)

            if form.is_valid():
                current_user = form.save()
                Contractor.objects.create(user=current_user, name=current_user.username)
                return redirect('login')
        context = {'form': form}
        return render(request, 'sign-up.html', context)


def home(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'sign-in.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)

        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logout(request):
    logout(request)
    return redirect('login')
