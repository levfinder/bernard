from django.contrib.auth.models import AbstractUser
from django.db import models

from bernard.core.enums import NotificationStatusEnum


class Organisation(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return '<Organisation: {}>'.format(self.__str__())


class User(AbstractUser):
    organisation = models.ForeignKey(
        Organisation, null=True, on_delete=models.PROTECT)


class Notification(models.Model):
    ref_id = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=32)
    email = models.EmailField(blank=True)
    key = models.CharField(max_length=48)

    trigger_datetime = models.DateTimeField()
    expiry_datetime = models.DateTimeField()

    status = models.CharField(
        max_length=16,
        choices=NotificationStatusEnum,
        default=NotificationStatusEnum.PENDING,
    )

    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)

    def __str__(self):
        return '{} {} {}'.format(
            self.vendor, self.ref_id, self.phone)

    def __repr__(self):
        return '<Notification: {}>'.format(self.__str__())


class Vehicle(models.Model):
    ref_id = models.CharField(max_length=16)
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.ref_id, self.vendor)

    def __repr__(self):
        return '<Vehicle: {}>'.format(self.__str__())

    class Meta:
        unique_together = ('ref_id', 'organisation')


class LocationUpdate(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.TimeField()

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.vehicle, self.timestamp)

    def __repr__(self):
        return '<LocationUpdate: {}>'.format(self.__str__())
