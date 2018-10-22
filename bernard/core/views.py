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

        return render(request, 'bernard/overview.html', ctx)

def order(request, id):
    if request.method == 'GET':
        ctx = {}

        ctx['mapping_api_id'] = settings.MAPPING_API_ID
        ctx['mapping_api_code'] = settings.MAPPING_API_CODE

        ctx['order'] = Order.objects.get(id=id)

        return render(request, 'bernard/order.html', ctx)

def vehicle(request, id):
    if request.method == 'GET':
        ctx = {}

        ctx['mapping_api_id'] = settings.MAPPING_API_ID
        ctx['mapping_api_code'] = settings.MAPPING_API_CODE

        ctx['vehicle'] = v = Vehicle.objects.get(id=id)

        ctx['location_history'] = \
             LocationUpdate.objects.filter(vehicle__id=id).order_by('timestamp')

        ctx['scheduled_deliveries'] = Delivery.objects.filter(vehicle__id=id)

        return render(request, 'bernard/vehicle.html', ctx)


def vehicles(request):
    if request.method == 'GET':
        return HttpResponse('')


def orders(request):
    if request.method == 'GET':
        return HttpResponse('')
