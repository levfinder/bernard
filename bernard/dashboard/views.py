from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ortools.constraint_solver import pywrapcp

from bernard.core.models import Driver, Stop

import googlemaps
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
            messages.error(request, 'Login failed')
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

        messages.info(request, 'You have been logged out')

        return redirect('login')


@login_required
def index(request):
    if request.method == 'GET':
        return redirect('drivers')


@login_required
def drivers(request):
    if request.method == 'GET':
        ctx = {}
        ctx['drivers'] = Driver.objects.all()
        ctx['googlemaps_key'] = settings.GOOGLE_MAPS_API_KEY

        return render(request, 'dashboard/drivers.html', ctx)


@login_required
def drivers_new(request):
    if request.method == 'GET':
        return render(request, 'dashboard/drivers_new.html')

    elif request.method == 'POST':
        name = request.POST.get('name')
        start_address = request.POST.get('start_address')

        if not name:
            messages.error(request, 'Name is required')
            return render(request, 'dashboard/drivers_new.html')

        if not start_address:
            messages.error(request, 'Start address is required')
            return render(request, 'dashboard/drivers_new.html')

        Driver.objects.create(
            name=name,
            start_address=start_address
        )

        return redirect('drivers')


@login_required
def driver(request, _id):
    if request.method == 'POST':
        _method = request.POST.get('_method')
        if _method == 'DELETE':
            Driver.objects.filter(id=_id).delete()
            return redirect('drivers')
        elif _method == 'PUT':
            pass


@login_required
def stops(request):
    if request.method == 'GET':
        ctx = {}

        ctx['stops'] = Stop.objects.all()
        ctx['googlemaps_key'] = settings.GOOGLE_MAPS_API_KEY

        return render(request, 'dashboard/stops.html', ctx)


@login_required
def stops_new(request):
    if request.method == 'GET':
        return render(request, 'dashboard/stops_new.html')

    elif request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')

        if not name:
            messages.error(request, 'Name is required')
            return render(request, 'dashboard/stops_new.html')

        if not address:
            messages.error(request, 'Address is required')
            return render(request, 'dashboard/stops_new.html')

        Stop.objects.create(
            name=name,
            address=address
        )

        return redirect('stops')


@login_required
def stop(request, _id):
    if request.method == 'POST':
        _method = request.POST.get('_method')
        if _method == 'DELETE':
            Stop.objects.filter(id=_id).delete()
            return redirect('stops')

        elif _method == 'PUT':
            pass


@login_required
def route(request):
    gm = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    addresses = [_.address for _ in Stop.objects.filter()]
    dist_matrix = gm.distance_matrix(origins=addresses, destinations=addresses)

    optimise_criteria = 'distance'
    matrix = []
    ctx = {}
    ctx['googlemaps_key'] = settings.GOOGLE_MAPS_API_KEY

    for element_obj in dist_matrix['rows']:
        row = []
        elements = element_obj['elements']
        for item in elements:
            row.append(item[optimise_criteria]['value'])
        matrix.append(row)

    tsp_size = len(addresses)
    num_routes = 1

    # start and end address index
    depot = 0

    def get_distance_callback(m):
        def distance_callback(from_node, to_node):
            return int(m[from_node][to_node])
        return distance_callback

    if tsp_size > 1:
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
                path.append(addresses[route.IndexToNode(index)])
                index = assignment.Value(route.NextVar(index))

            path.append(addresses[route.IndexToNode(index)])

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
def settings_account(request):
    if request.method == 'GET':
        return render(request, 'dashboard/settings_account.html')
    elif request.method == 'POST':
        if not request.POST.get('password', ''):
            messages.error(request, 'Old password is required')
            return render(request, 'dashboard/settings_account.html')

        old_password = request.POST.get('password', '')
        if not request.user.check_password(old_password):
            messages.error(request, 'Incorrect password')
            return render(request, 'dashboard/settings_account.html')

        if request.POST.get('new_password') \
                or request.POST.get('new_password_confirm'):
            if request.POST.get('new_password') != \
                    request.POST.get('new_password_confirm'):
                messages.error(request, 'New passwords do not match')
                return render(request, 'dashboard/settings_account.html')
            else:
                request.user.set_password(request.POST.get('new_password'))

        # TODO validate email
        if not request.POST.get('email', ''):
            messages.error(request, 'Email is required')
            return render(request, 'dashboard/settings_account.html')

        email = request.POST.get('email')
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            messages.error(request, 'Invalid email')
            return render(request, 'dashboard/settings_account.html')

        request.user.email = email
        request.user.save()

        messages.info(request, 'Changes saved')
        return render(request, 'dashboard/settings_account.html')


@login_required
def settings_api(request):
    if request.method == 'GET':
        return render(request, 'dashboard/settings_api.html')
