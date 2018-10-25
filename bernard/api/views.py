from rest_framework import viewsets

from bernard.core.models import Delivery, Order, Vehicle, Vendor
from bernard.api.serializers import DeliverySerializer, OrderSerializer,\
    VehicleSerializer, VendorSerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all().order_by('-timeslot')
    serializer_class = DeliverySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
