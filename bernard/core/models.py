from django.contrib.auth.models import AbstractUser
from django.db import models

from bernard.core.enums import NotificationStatusEnum

import random
import string
import uuid


class Organisation(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return '<Organisation: {}>'.format(self.__str__())


class User(AbstractUser):
    organisation = models.ForeignKey(
        Organisation, null=True, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if 'pbkdf2_sha256' not in self.password:
            self.set_password(self.password)

        self.username = self.username.lower()
        self.email = self.email.lower()

        super(User, self).save(*args, **kwargs)

        return self


class Vehicle(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)

    # licence registration
    ref_id = models.CharField(max_length=16)

    # descriptive text about vehicle
    info = models.CharField(max_length=256, blank=True, default='')

    # app key
    app_login_key = models.CharField(max_length=16, blank=True, default='')

    def save(self, *args, **kwargs):
        if not self.app_login_key:
            self.app_login_key = '{}{}'.format(
                ''.join(random.choice(string.ascii_uppercase)
                        for _ in range(4)),
                ''.join(random.choice(string.digits)
                        for _ in range(4)))
        super(Vehicle, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return '{} {}'.format(self.ref_id, self.organisation)

    def __repr__(self):
        return '<Vehicle: {}>'.format(self.__str__())

    def get_absolute_url(self):
        return '/vehicles/{}'.format(self.id)

    class Meta:
        unique_together = ('ref_id', 'organisation')


class Notification(models.Model):
    ref_id = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=32)
    email = models.EmailField(blank=True)
    tracking_key = models.CharField(max_length=48, blank=True, default='')

    trigger_datetime = models.DateTimeField()
    expiry_datetime = models.DateTimeField()

    status = models.CharField(
        max_length=16,
        choices=NotificationStatusEnum,
        default=NotificationStatusEnum.PENDING,
    )

    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.tracking_key:
            self.tracking_key = str(uuid.uuid4()).replace('-', '')
        super(Notification, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return '{} {} {}'.format(
            self.organisation, self.ref_id, self.phone)

    def __repr__(self):
        return '<Notification: {}>'.format(self.__str__())

    def get_absolute_url(self):
        return '/notifications/{}'.format(self.id)


class LocationUpdate(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.TimeField()

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.vehicle, self.timestamp)

    def __repr__(self):
        return '<LocationUpdate: {}>'.format(self.__str__())
