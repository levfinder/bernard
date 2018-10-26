from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from bernard.core.models import LocationUpdate, Notification, Organisation, \
    Vehicle
from bernard.core.enums import NotificationStatusEnum


def login_view(request):
    if request.method == 'GET':
        next_path = request.GET.get('next', '/')

        return render(request, 'bernard/login.html', {'next_path': next_path})

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_path = request.POST.get('next', '/')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(
                request, 'bernard/login.html',
                {'message': 'Login failed', 'next_path': next_path})
        else:
            login(request, user)
            return redirect(next_path)


def logout_view(request):
    if request.method == 'GET':
        logout(request)

        return redirect('login')


@login_required
def overview(request):
    if request.method == 'GET':
        ctx = dict()
        ctx['settings'] = settings

        return render(request, 'bernard/overview.html', ctx)


@login_required
def notification(request, id):
    if request.method == 'GET':
        return render(request, 'bernard/notification.html')


@login_required
def notifications(request):
    if request.method == 'GET':
        return render(request, 'bernard/notifications.html')


@login_required
def vehicle(request, id):
    if request.method == 'GET':
        ctx = dict()
        ctx['settings'] = settings

        ctx['vehicle'] = Vehicle.objects.get(id=id)

        ctx['location_history'] = \
            LocationUpdate.objects.filter(vehicle__id=id).order_by('timestamp')

        return render(request, 'bernard/vehicle.html', ctx)


@login_required
def vehicles(request):
    if request.method == 'GET':
        ctx = dict()
        ctx['settings'] = settings

        ctx['vehicles'] = Vehicle.objects.all()

        return render(request, 'bernard/vehicles.html', ctx)
