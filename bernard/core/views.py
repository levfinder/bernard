from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.conf import settings

from bernard.core.models import Order, Vehicle, LocationUpdate, Delivery


def overview(request):
    if request.method == 'GET':
        ctx = {}

        ctx['unscheduled_orders'] = Order.objects.filter(delivery__order=None)
        ctx['scheduled_orders'] = Order.objects.filter(~Q(delivery__order=None))
        ctx['vehicles'] = Vehicle.objects.all()

        return render(request, 'overview.html', ctx)

def order(request, id):
    if request.method == 'GET':
        ctx = {}

        ctx['order'] = Order.objects.get(id=id)

        return render(request, 'order.html', ctx)

def vehicle(request, id):
    if request.method == 'GET':
        ctx = {}

        ctx['vehicle'] = v = Vehicle.objects.get(id=id)
        hist_loc = LocationUpdate.objects.filter(vehicle__id=id).order_by('timestamp')

        route = ','.join(['{},{}'.format(_.latitude, _.longitude) for _ in hist_loc])
        last_loc = '{},{}'.format(hist_loc.last().latitude, hist_loc.last().longitude)

        ctx['map_url'] = 'https://image.maps.api.here.com/mia/1.6/route?app_id={}&app_code={}&r0={}&m0={}'.format(settings.MAPPING_API_ID, settings.MAPPING_API_CODE, route, last_loc)

        ctx['scheduled_deliveries'] = Delivery.objects.filter(vehicle__id=id)

        return render(request, 'vehicle.html', ctx)

