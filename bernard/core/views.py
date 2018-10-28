from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from bernard.core.models import LocationUpdate, Notification, Organisation, \
    Vehicle
from bernard.core.enums import NotificationStatusEnum

import datetime
import uuid


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
    ctx = dict()

    if request.method == 'GET':
        ctx['settings'] = settings

        return render(request, 'bernard/overview.html', ctx)


@login_required
def notification(request, id):
    ctx = dict()
    if request.method == 'GET':

        ctx['notification'] = Notification.objects.get(id=id)

        return render(request, 'bernard/notification.html', ctx)


@login_required
def notifications(request):
    ctx = dict()
    if request.method == 'GET':

        organisation = getattr(request.user, 'organisation', None)

        if not organisation:
            ctx['notifications'] = Notification.objects.all()
        else:
            ctx['notifications'] = Notification.objects.filter(
                organisation=organisation.id)

        return render(request, 'bernard/notifications.html', ctx)


@login_required
def notification_new(request):
    ctx = dict()

    if request.method == 'GET':
        ctx['now'] = datetime.datetime.now().timestamp()

        organisation = getattr(request.user, 'organisation', None)

        if not organisation:
            # user is admin, show org field
            ctx['vehicles'] = Vehicle.objects.all()
            ctx['organisations'] = Organisation.objects.all()
        else:
            ctx['vehicles'] = Vehicle.objects.filter(
                organisation=organisation.id)

        return render(request, 'bernard/notification_new.html', ctx)
    elif request.method == 'POST':
        trigger = datetime.datetime.strptime(
            request.POST.get('trigger_datetime'), '%Y-%m-%d %H:%M')
        expiry = datetime.datetime.strptime(
            request.POST.get('expiry_datetime'), '%Y-%m-%d %H:%M')

        ref_id = request.POST.get('ref_id')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')

        organisation = getattr(request.user, 'organisation', None)

        if not organisation:
            # user is admin
            organisation = Organisation.objects.get(
                id=int(request.POST.get('organisation', '-1')))

        vehicle = Vehicle.objects.get(
            id=int(request.POST.get('vehicle', '-1')))
        key = str(uuid.uuid4()).replace('-', '')

        Notification.objects.create(
            ref_id=ref_id,
            phone=phone,
            email=email,
            key=key,
            trigger_datetime=trigger,
            expiry_datetime=expiry,
            organisation=organisation,
            vehicle=vehicle
        )

        messages.add_message(
            request, messages.INFO, 'Notification object created')

        return redirect('notifications')


@login_required
def vehicle(request, id):
    ctx = dict()

    if request.method == 'GET':
        ctx['settings'] = settings

        ctx['vehicle'] = Vehicle.objects.get(id=id)

        ctx['location_history'] = \
            LocationUpdate.objects.filter(vehicle__id=id).order_by('timestamp')

        return render(request, 'bernard/vehicle.html', ctx)


@login_required
def vehicles(request):
    ctx = dict()

    if request.method == 'GET':
        ctx['settings'] = settings

        ctx['vehicles'] = Vehicle.objects.all()

        return render(request, 'bernard/vehicles.html', ctx)


@login_required
def vehicle_new(request):
    ctx = dict()

    if request.method == 'GET':
        organisation = getattr(request.user, 'organisation', None)

        if not organisation:
            # user is admin, show org field
            ctx['organisations'] = Organisation.objects.all()

        return render(request, 'bernard/vehicle_new.html', ctx)

    elif request.method == 'POST':
        ref_id = request.POST.get('ref_id')
        info = request.POST.get('info')

        organisation = getattr(request.user, 'organisation', None)

        if not organisation:
            # user is admin
            organisation = Organisation.objects.get(
                id=int(request.POST.get('organisation', '-1')))

        Vehicle.objects.create(
            ref_id=ref_id,
            info=info,
            organisation=organisation,
        )

        return redirect('vehicles')


@login_required
def tokens(request):
    if request.method == 'GET':
        return render(request, 'bernard/tokens.html')


def track(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        notif = Notification.objects.get(key=key)

        if notif:
            pass

        else:
            pass
