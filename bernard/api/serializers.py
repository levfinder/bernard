from rest_framework import serializers

from bernard.core.models import Delivery, Order, Vehicle, Vendor


class DeliverySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Delivery
        fields = ('timeslot', 'status', 'order', 'vehicle')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('external_id', 'street', 'city', 'postcode', 'phone',
                  'email', 'vendor')


class VehicleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('external_id', 'vendor')


class VendorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendor
        fields = ('name')
