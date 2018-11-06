from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'GET':
        next_path = request.GET.get('next', '/')

        return render(
            request, 'dashboard/login.html', {'next_path': next_path})

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_path = request.POST.get('next', '/')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(
                request, 'dashboard/login.html',
                {'message': 'Login failed', 'next_path': next_path})
        else:
            login(request, user)
            return redirect(next_path)


def logout_view(request):
    if request.method == 'GET':
        logout(request)

        return redirect('login')


@login_required
def index(request):
    if request.method == 'GET':
        return redirect('drivers')


@login_required
def drivers(request):
    if request.method == 'GET':
        return render(request, 'dashboard/drivers.html')


@login_required
def stops(request):
    if request.method == 'GET':
        return render(request, 'dashboard/stops.html')


@login_required
def settings_view(request):
    if request.method == 'GET':
        return redirect('settings_account')


@login_required
def settings_account(request):
    if request.method == 'GET':
        return render(request, 'dashboard/settings_account.html')


@login_required
def settings_api(request):
    if request.method == 'GET':
        return render(request, 'dashboard/settings_api.html')
