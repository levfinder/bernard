from django.shortcuts import render, redirect
from django.conf import settings

from bernard.core.models import Order, Vehicle, LocationUpdate, Delivery
from bernard.core.enums import DeliveryStatusEnum

import datetime


def overview(request):
    if request.method == 'GET':
        ctx = dict()

        ctx['unscheduled_orders'] = Order.objects.filter(delivery__order=None)
        ctx['vehicles'] = Vehicle.objects.all()
        ctx['scheduled_deliveries'] = Delivery.objects.filter(
            status=DeliveryStatusEnum.SCHEDULED)

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
        ctx = dict()

        ctx['mapping_api_id'] = settings.MAPPING_API_ID
        ctx['mapping_api_code'] = settings.MAPPING_API_CODE

        ctx['vehicle'] = Vehicle.objects.get(id=id)

        ctx['location_history'] = \
            LocationUpdate.objects.filter(vehicle__id=id).order_by('timestamp')

        ctx['scheduled_deliveries'] = Delivery.objects.filter(vehicle__id=id)

        return render(request, 'bernard/vehicle.html', ctx)


def vehicles(request):
    if request.method == 'GET':
        ctx = dict()
        ctx['vehicles'] = Vehicle.objects.all()
        return render(request, 'bernard/vehicles.html', ctx)


def orders(request):
    if request.method == 'GET':
        ctx = dict()
        ctx['orders'] = Order.objects.all()
        return render(request, 'bernard/orders.html', ctx)


def deliveries_new(request):
    if request.method == 'GET':
        ctx = dict()

        ctx['vehicles'] = Vehicle.objects.all()
        ctx['orders'] = Order.objects.all()

        ctx['vehicle_id'] = int(request.GET.get('vehicle', -1))
        ctx['order_id'] = int(request.GET.get('order', -1))

        return render(request, 'bernard/deliveries_new.html', ctx)

    elif request.method == 'POST':
        ctx = dict()

        vehicle_id = int(request.POST.get('vehicle_id'))
        order_id = int(request.POST.get('order_id'))
        timeslot = datetime.datetime.strptime(
            request.POST.get('timeslot'),
            '%Y-%m-%d %H:%M',
        )

        vehicle = Vehicle.objects.get(id=vehicle_id)
        order = Order.objects.get(id=order_id)

        Delivery.objects.create(
            order=order,
            vehicle=vehicle,
            timeslot=timeslot,
            status=DeliveryStatusEnum.SCHEDULED
        )

        return redirect(vehicle)
