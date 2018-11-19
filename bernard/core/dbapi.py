from django.core.exceptions import ObjectDoesNotExist

from bernard.core.models import Address, Stop, Driver


def get_address(**kwargs):
    try:
        return Address.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None


def get_driver(**kwargs):
    try:
        return Driver.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None


def create_address(**kwargs):
    address = Address.objects.create(**kwargs)
    return address


def create_driver(**kwargs):
    driver = Driver.objects.create(**kwargs)
    return driver


def create_stop(**kwargs):
    stop = Stop.objects.create(**kwargs)
    return stop


def delete_address(address_id):
    Address.objects.filter(id=address_id).delete()


def delete_driver(driver_id):
    Driver.objects.filter(id=driver_id).delete()


def delete_stop(stop_id):
    Stop.objects.filter(id=stop_id).delete()
