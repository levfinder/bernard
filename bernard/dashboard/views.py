import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from ortools.constraint_solver import pywrapcp

from bernard.core.dbapi import get_address, create_address, create_stop, \
    create_driver, delete_driver, delete_stop, get_driver
from bernard.core.models import Driver, Stop
from bernard.core.utils import get_distance_matrix


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
                 'lf_env': settings.LF_ENVIRONMENT})
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

        if not ctx['drivers']:
            messages.info(request, _('No drivers found'))

        return render(request, 'dashboard/drivers.html', ctx)


@login_required
def drivers_new_view(request):
    ctx = {}
    ctx['googlemaps_key'] = settings.GOOGLE_MAPS_API_KEY

    if request.method == 'GET':
        return render(request, 'dashboard/drivers_new.html', ctx)

    elif request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        travel_mode = int(request.POST.get('travel_mode', 0))

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

            return render(request, 'dashboard/drivers_new.html', ctx)

        address = get_address(
            street_number=street_number,
            street_name=route,
            city=postal_town,
            post_code=postal_code,
            country=country,
        )

        if not address:
            address = create_address(
                street_number=street_number,
                street_name=route,
                city=postal_town,
                post_code=postal_code,
                country=country,
                latitude=float(latitude),
                longitude=float(longitude)
            )

        create_driver(
            name=name,
            start_address=address,
            phone=phone,
            travel_mode=travel_mode,
        )

        return redirect('drivers')


@login_required
def driver_view(request, driver_id):
    if request.method == 'POST':
        _method = request.POST.get('_method')

        if _method == 'DELETE':
            delete_driver(driver_id)
            return redirect('drivers')

        elif _method == 'PUT':
            pass


@login_required
def stops_view(request):
    ctx = {}
    ctx['googlemaps_key'] = settings.GOOGLE_MAPS_API_KEY

    if request.method == 'GET':
        ctx['stops'] = Stop.objects.all()

        if not ctx['stops']:
            messages.info(request, _('No stops found'))

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

        address = get_address(latitude=lat, longitude=lng)

        if not address:
            address = create_address(
                street_number=street_number,
                street_name=route,
                city=postal_town,
                post_code=postal_code,
                country=country,
                latitude=lat,
                longitude=lng,
            )

        create_stop(
            name=name,
            address=address
        )

        return redirect('stops')


@login_required
def stop_view(request, stop_id):
    if request.method == 'POST':
        _method = request.POST.get('_method')

        if _method == 'DELETE':
            delete_stop(stop_id)
            return redirect('stops')

        elif _method == 'PUT':
            pass


@login_required
def route_view(request):
    ctx = {}
    ctx['googlemaps_key'] = settings.GOOGLE_MAPS_API_KEY

    if request.method == 'GET':
        ctx['drivers'] = Driver.objects.all()

        if not ctx['drivers']:
            messages.info(request, _('No drivers found'))

        return render(request, 'dashboard/route.html', ctx)

    elif request.method == 'POST':
        driver_id = int(request.POST.get('driver'))
        stops = Stop.objects.filter()
        driver = get_driver(id=driver_id)

        if not stops:
            messages.info(request, _('No stops found'))
            return render(request, 'dashboard/route.html', ctx)

        stop_addresses = [_.address for _ in stops]
        stop_addresses.insert(0, driver.start_address)

        stop_names = [_.name for _ in stops]
        stop_names.insert(0, '')

        tsp_size = len(stop_addresses)
        num_routes = 1

        if tsp_size > 11:
            messages.warning(request, _('Total stops cannot exceed 10'))
            return render(request, 'dashboard/route.html', ctx)

        matrix = get_distance_matrix(stop_addresses)

        optimise_criteria = 'distance'

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
            path_names = []

            while not route.IsEnd(index):
                path.append(stop_addresses[route.IndexToNode(index)])
                path_names.append(stop_names[route.IndexToNode(index)])
                index = assignment.Value(route.NextVar(index))

            path.append(stop_addresses[route.IndexToNode(index)])
            path_names.append(stop_names[route.IndexToNode(index)])

            ctx['path'] = path
            ctx['stops'] = zip(path, path_names)
            ctx['distance'] = '{} {}'.format(
                total_distance,
                'm' if optimise_criteria == 'distance' else 'seconds'
            )

        ctx['driver'] = driver

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
