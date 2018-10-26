from rest_framework import serializers

from bernard.core.models import Notification, Vehicle


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ('phone', 'email', 'trigger_datetime', 'expiry_datetime')


class VehicleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('external_id')
