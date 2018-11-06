#!/usr/bin/env python3

import faker
import random
import uuid

from django_seed import Seed

from bernard.core.models import User, Driver, Stop


addresses = [
    'Landalabergen 18',
    'Föreningsgatan 15',
    'Medicinaregatan 2',
    'Dr Lindhs gata 1',
    'Kjellmansgatan 7',
    'Mejerigatan 2',
    'Richertsgatan 2B',
    'Brahegatan 9',
    'Marconigatan 7',
    'Näverlursgatan 32',
    'Utlandagatan 24',
    'Gånglåten 5',
    'Studiegången 6',
    'Kapellgången 1',
    'Gibraltargatan 84',
    'Plejadgatan 7',
    'Rännvägen 1',
]


seeder = Seed.seeder()
fake = faker.Faker(locale='sv_SE')

seeder.add_entity(Driver, 3, {
    'name': lambda x: fake.license_plate(),
    'start_address': lambda x: random.choice(addresses),
})

seeder.add_entity(Stop, 10, {
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
        if not User.objects.filter(username=user[0]):
            User.objects.create(
                username=user[0],
                email=user[1],
                password='levtest123',
            )
