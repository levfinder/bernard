from rest_framework import viewsets

from bernard.core.models import Notification, Vehicle
from bernard.api.serializers import NotificationSerializer, VehicleSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
