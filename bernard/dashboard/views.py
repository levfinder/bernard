from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from ortools.constraint_solver import pywrapcp

from bernard.core.models import Driver, Stop, Address
from bernard.core.utils import get_distance_matrix

import re


def login_view(request):
    if request.method == 'GET':
        next_path = request.GET.get('next', '/')

        return render(
            request, 'dashboard/login.html',
            {'next_path': next_path,
             'lf_env': settings.LF_ENVIRONMENT})

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_path = request.POST.get('next', '/')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, _('Login failed'))
            return render(
                request, 'dashboard/login.html',
                {'next_path': next_path,
                 'is_prod': settings.LF_ENVIRONMENT == 'prod'})
        else:
            login(request, user)
            return redirect(next_path)


def logout_view(request):
    if request.method == 'GET':
        logout(request)

        messages.info(request, _('You have been logged out'))

        return redirect('login')


@login_required
def index_view(request):
    if request.method == 'GET':
        return redirect('drivers')


@login_required
def drivers_view(request):
    ctx = {}
    ctx['googlemaps_key'] = settings.GOOGLE_MAPS_API_KEY

    if request.method == 'GET':
        ctx['drivers'] = Driver.objects.all()

        return render(request, 'dashboard/drivers.html', ctx)


@login_required
def drivers_new_view(request):
    ctx = {}
    ctx['googlemaps_key'] = settings.GOOGLE_MAPS_API_KEY

    if request.method == 'GET':
        return render(request, 'dashboard/drivers_new.html', ctx)

    elif request.method == 'POST':
        name = request.POST.get('name')

        street_number = request.POST.get('street_number')
        route = request.POST.get('route')
        postal_town = request.POST.get('postal_town')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')

        latitude = request.POST.get('latitude', 0.0)
        longitude = request.POST.get('longitude', 0.0)

        if not name:
            messages.error(request, _('Name is required'))
            return render(request, 'dashboard/drivers_new.html', ctx)

        if not (street_number and route and postal_town and country and
                postal_code and latitude and longitude):
            if not street_number:
                messages.error(request, _('Valid street number is required'))
            else:
                messages.error(request, _('Valid address is required'))
            return render(request, 'dashboard/stops_new.html', ctx)

        address = Address.objects.create(
            street_number=street_number,
            street_name=route,
            city=postal_town,
            post_code=postal_code,
            country=country,
            latitude=float(latitude),
            longitude=float(longitude)
        )

        Driver.objects.create(
            name=name,
            start_address=address
        )

        return redirect('drivers')


@login_required
def driver_view(request, _id):
    if request.method == 'POST':
        _method = request.POST.get('_method')
        if _method == 'DELETE':
            Driver.objects.filter(id=_id).delete()
            return redirect('drivers')
        elif _method == 'PUT':
            pass


@login_required
def stops_view(request):
    ctx = {}
    ctx['googlemaps_key'] = settings.GOOGLE_MAPS_API_KEY

    if request.method == 'GET':
        ctx['stops'] = Stop.objects.all()

        return render(request, 'dashboard/stops.html', ctx)


@login_required
def stops_new_view(request):
    ctx = {}
    ctx['googlemaps_key'] = settings.GOOGLE_MAPS_API_KEY

    if request.method == 'GET':
        return render(request, 'dashboard/stops_new.html', ctx)

    elif request.method == 'POST':
        name = request.POST.get('name')

        street_number = request.POST.get('street_number')
        route = request.POST.get('route')
        postal_town = request.POST.get('postal_town')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')

        latitude = request.POST.get('latitude', 0.0)
        longitude = request.POST.get('longitude', 0.0)

        if not name:
            messages.error(request, _('Name is required'))
            return render(request, 'dashboard/stops_new.html', ctx)

        if not (route and postal_town and country and postal_code and
                latitude and longitude):
            if not street_number:
                messages.error(request, _('Valid street number is required'))
            else:
                messages.error(request, _('Valid address is required'))
            return render(request, 'dashboard/stops_new.html', ctx)

        lat = round(float(latitude), 5)
        lng = round(float(longitude), 5)
        addr_q = Address.objects.filter(latitude=lat, longitude=lng)

        if not addr_q:
            addr = Address.objects.create(
                street_number=street_number,
                street_name=route,
                city=postal_town,
                post_code=postal_code,
                country=country,
                latitude=lat,
                longitude=lng,
            )
        else:
            addr = addr_q[0]

        Stop.objects.create(
            name=name,
            address=addr
        )

        return redirect('stops')


@login_required
def stop_view(request, _id):
    if request.method == 'POST':
        _method = request.POST.get('_method')
        if _method == 'DELETE':
            Stop.objects.filter(id=_id).delete()
            return redirect('stops')

        elif _method == 'PUT':
            pass


@login_required
def route_view(request):
    ctx = {}
    ctx['googlemaps_key'] = settings.GOOGLE_MAPS_API_KEY

    stops = Stop.objects.filter()
    driver = Driver.objects.get(id=1)

    stop_addresses = [_.address for _ in stops]
    stop_addresses.insert(0, driver.start_address)

    matrix = get_distance_matrix(stop_addresses)

    optimise_criteria = 'distance'

    tsp_size = len(stop_addresses)
    num_routes = 1

    # start and end address index
    depot = 0

    def get_distance_callback(m):
        def distance_callback(from_node, to_node):
            return int(m[from_node][to_node])
        return distance_callback

    route = pywrapcp.RoutingModel(tsp_size, num_routes, depot)

    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

    dist_callback = get_distance_callback(matrix)
    route.SetArcCostEvaluatorOfAllVehicles(dist_callback)

    assignment = route.SolveWithParameters(search_parameters)

    if assignment:
        total_distance = assignment.ObjectiveValue()

        route_number = 0
        index = route.Start(route_number)

        path = []

        while not route.IsEnd(index):
            path.append(stop_addresses[route.IndexToNode(index)])
            index = assignment.Value(route.NextVar(index))
        path.append(stop_addresses[route.IndexToNode(index)])

        ctx['path'] = path
        ctx['distance'] = '{} {}'.format(
            total_distance,
            'm' if optimise_criteria == 'distance' else 'seconds'
        )

    return render(request, 'dashboard/route.html', ctx)


@login_required
def settings_view(request):
    if request.method == 'GET':
        return redirect('settings_account')


@login_required
def settings_account_view(request):
    if request.method == 'GET':
        return render(request, 'dashboard/settings_account.html')
    elif request.method == 'POST':
        if not request.POST.get('password', ''):
            messages.error(request, _('Old password is required'))
            return render(request, 'dashboard/settings_account.html')

        old_password = request.POST.get('password', '')
        if not request.user.check_password(old_password):
            messages.error(request, _('Incorrect password'))
            return render(request, 'dashboard/settings_account.html')

        if request.POST.get('new_password') \
                or request.POST.get('new_password_confirm'):
            if request.POST.get('new_password') != \
                    request.POST.get('new_password_confirm'):
                messages.error(request, _('New passwords do not match'))
                return render(request, 'dashboard/settings_account.html')
            else:
                request.user.set_password(request.POST.get('new_password'))

        # TODO validate email
        if not request.POST.get('email', ''):
            messages.error(request, _('Email is required'))
            return render(request, 'dashboard/settings_account.html')

        email = request.POST.get('email')
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            messages.error(request, _('Invalid email'))
            return render(request, 'dashboard/settings_account.html')

        request.user.email = email
        request.user.save()

        messages.info(request, _('Changes saved'))
        return render(request, 'dashboard/settings_account.html')


@login_required
def settings_api_view(request):
    if request.method == 'GET':
        return render(request, 'dashboard/settings_api.html')
