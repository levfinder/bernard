#!/usr/bin/env python3

import faker
import random
import uuid

from django_seed import Seed

from bernard.core.models import User, Driver, Stop


addresses = [
    "Vasagatan 13, Gothenburg",
    "Kungsportsavenyen 10, Gothenburg",
    "Haga Nygata 16, Gothenburg",
    "Majorsgatan 1, Gothenburg",
    "Viktoriagatan 19, Gothenburg",
    "Terrassgatan 3, Gothenburg",
    "Fredsgatan 14, Gothenburg",
    "Kyrkogatan 13, Gothenburg",
    "Herkulesgatan 13, Gothenburg",
    "Västra Keillersgatan 9, Gothenburg",
]


seeder = Seed.seeder()
fake = faker.Faker(locale='sv_SE')

seeder.add_entity(Driver, 3, {
    'name': lambda x: fake.license_plate(),
    'start_address': lambda x: random.choice(addresses),
})

seeder.add_entity(Stop, 50, {
    'name': lambda x: str(uuid.uuid4()).replace('-', ''),
    'address': lambda x: random.choice(addresses),
})


def run(*args):
    seeder.execute()

    default_users = [
        ('viren', 'viren@levfinder.se'),
        ('kruslock', 'christoffer@levfinder.se')
    ]

    for user in default_users:
        if not User.objects.get(username=user[0]):
            User.objects.create(
                username=user[0],
                email=user[1],
                password='levtest123',
            )
