from django.db import models

from bernard.core.enums import DeliveryStatusEnum


class Vendor(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return '<Vendor: {}>'.format(self.__str__())


class Order(models.Model):
    external_id = models.CharField(max_length=32)

    street = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    postcode = models.CharField(max_length=16)

    phone = models.CharField(max_length=32)
    email = models.EmailField()

    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)

    def __str__(self):
        return '{} {} {} {}'.format(
            self.vendor, self.external_id, self.street, self.city)

    def __repr__(self):
        return '<Order: {}>'.format(self.__str__())


class Vehicle(models.Model):
    external_id = models.CharField(max_length=16)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.vendor, self.external_id)

    def __repr__(self):
        return '<Vehicle: {}>'.format(self.__str__())


class Delivery(models.Model):
    timeslot = models.DateTimeField()
    status = models.CharField(max_length=32, choices=DeliveryStatusEnum)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.order, self.timeslot)

    def __repr__(self):
        return '<Delivery: {}>'.format(self.__str__())


class LocationUpdate(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.TimeField()

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.vehicle, self.timestamp)

    def __repr__(self):
        return '<LocationUpdate: {}>'.format(self.__str__())
