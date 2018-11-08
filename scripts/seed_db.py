#!/usr/bin/env python3

import faker
import random
import uuid

from django_seed import Seed

from bernard.core.models import User, Driver, Stop


addresses = [
    'Landalabergen 18, Göteborg',
    'Föreningsgatan 15, Göteborg',
    'Medicinaregatan 2, Göteborg',
    'Dr Lindhs gata 1, Göteborg',
    'Kjellmansgatan 7, Göteborg',
    'Mejerigatan 2, Göteborg',
    'Richertsgatan 2B, Göteborg',
    'Brahegatan 9, Göteborg',
    'Marconigatan 7, Göteborg',
    'Näverlursgatan 32, Göteborg',
    'Utlandagatan 24, Göteborg',
    'Gånglåten 5, Göteborg',
    'Studiegången 6, Göteborg',
    'Kapellgången 1, Göteborg',
    'Gibraltargatan 84, Göteborg',
    'Plejadgatan 7, Göteborg',
    'Rännvägen 1, Göteborg',
    'Stjernsköldsgatan 14, Göteborg',
    'Donsögatan 7, Göteborg',
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
