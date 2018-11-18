from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def save(self, *args, **kwargs):
        if 'pbkdf2_sha256' not in self.password:
            self.set_password(self.password)

        self.username = self.username.lower()
        self.email = self.email.lower()

        super(User, self).save(*args, **kwargs)

        return self


class Address(models.Model):
    street_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    post_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)

    def __str__(self):
        return '{} {} {}'.format(
            self.street_name, self.street_number, self.city)

    def __repr__(self):
        return '<Address: {}>'.format(self.__str__())

    class Meta:
        verbose_name_plural = 'addresses'


class SpatialDistance(models.Model):
    origin = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name='OriginAddress')
    destination = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name='DestinationAddress')

    value = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        unique_together = ('origin', 'destination')


class Driver(models.Model):
    name = models.CharField(max_length=150)
    start_address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return '<Driver: {}>'.format(self.__str__())


class Stop(models.Model):
    name = models.CharField(max_length=150)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.name, self.address)

    def __repr__(self):
        return '<Stop: {}>'.format(self.__str__())
