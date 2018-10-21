#!/usr/bin/env python3

import datetime
import uuid

from django_seed import Seed
from bernard.core.models import Vendor, Order, Vehicle, Delivery, LocationUpdate


seeder = Seed.seeder(locale='sv_SE')

seeder.add_entity(Vendor, 5, {
    'name': lambda x: seeder.faker.company(),
})

seeder.add_entity(Vehicle, 10, {
    'external_id': lambda x: seeder.faker.license_plate(),
})

seeder.add_entity(LocationUpdate, 50, {
    'latitude': lambda x: seeder.faker.latitude(),
    'latitude': lambda x: seeder.faker.longitude(),
})

seeder.add_entity(Order, 20, {
    'external_id': lambda x: uuid.uuid4(),
    'street': lambda x: seeder.faker.street_address(),
    'city': lambda x: seeder.faker.city(),
    'postcode': lambda x: seeder.faker.postcode(),
    'phone': lambda x: seeder.faker.phone_number(),
    'email': lambda x: seeder.faker.ascii_email(),
})

def run(*args):
    seeder.execute()

