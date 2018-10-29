#!/usr/bin/env python3

import faker
import uuid

from django_seed import Seed

from bernard.core.models import Organisation, Notification, Vehicle, \
    LocationUpdate


seeder = Seed.seeder()
fake = faker.Faker(locale='sv_SE')

seeder.add_entity(Organisation, 3, {
    'name': lambda x: fake.company(),
})

seeder.add_entity(Vehicle, 10, {
    'ref_id': lambda x: fake.license_plate(),
})

seeder.add_entity(LocationUpdate, 50, {
    'latitude': lambda x: fake.latitude(),
    'longitude': lambda x: fake.longitude(),
})

seeder.add_entity(Notification, 20, {
    'ref_id': lambda x: str(uuid.uuid4()).replace('-', ''),
    'phone': lambda x: fake.phone_number(),
    'email': lambda x: fake.ascii_email(),
    'key': lambda x: str(uuid.uuid4()).replace('-', ''),
})


def run(*args):
    seeder.execute()
