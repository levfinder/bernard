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


class Driver(models.Model):
    name = models.CharField(max_length=150)
    start_address = models.CharField(max_length=300)

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return '<Driver: {}>'.format(self.__str__())


class Stop(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=300)

    def __str__(self):
        return '{} {}'.format(self.name, self.address)

    def __repr__(self):
        return '<Stop: {}>'.format(self.__str__())
