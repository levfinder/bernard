from django.db import models

from bernard.core.enums import DeliveryStatusEnum


class Vendor(models.Model):
    name = models.CharField(max_length=64)


class Order(models.Model):
    external_id = models.CharField(max_length=32)

    street = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    postcode = models.CharField(max_length=16)

    phone = models.CharField(max_length=32)
    email = models.EmailField()

    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)


class Vehicle(models.Model):
    external_id = models.CharField(max_length=16)

    # TODO is there a one-to-one between Vehicle and Vendor?


class Delivery(models.Model):
    timeslot = models.DateTimeField()
    status = models.CharField(
        max_length=8,
        choices=[(tag, tag.value) for tag in DeliveryStatusEnum]
    )
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.TimeField()

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
