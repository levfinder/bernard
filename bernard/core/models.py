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

    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return '{} {} {}'.format(
            self.street_name, self.street_number, self.city)

    def __repr__(self):
        return '<Address: {}>'.format(self.__str__())

    class Meta:
        verbose_name_plural = 'addresses'


class Driver(models.Model):
    name = models.CharField(max_length=150)
    start_address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return '<Driver: {}>'.format(self.__str__())


class Stop(models.Model):
    name = models.CharField(max_length=150)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.name, self.address)

    def __repr__(self):
        return '<Stop: {}>'.format(self.__str__())
