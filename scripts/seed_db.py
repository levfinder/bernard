#!/usr/bin/env python3

import faker
import uuid

from collections import namedtuple
from django_seed import Seed

from bernard.core.models import User, Driver, Stop, Address


Addr = namedtuple('Addr', 'street_name, street_number, city, postcode,'
                  'country, lat, lng')

addresses = [
    Addr('Landalabergen', '18', 'Göteborg', '411 29', 'Sweden',
         57.6930887, 11.968833),
    Addr('Föreningsgatan', '15', 'Göteborg', '411 27', 'Sweden',
         57.6947052, 11.9646174),
    Addr('Medicinaregatan', '2', 'Göteborg', '413 46', 'Sweden',
         57.6845968, 11.9625556),
    Addr('Dr Lindhs gata', '1', 'Göteborg', '413 25', 'Sweden',
         57.6818506, 11.9676563),
    Addr('Kjellmansgatan', '7', 'Göteborg', '413 18', 'Sweden',
         57.69781349999999, 11.9386905),
    Addr('Mejerigatan', '2', 'Göteborg', '412 76', 'Sweden',
         57.68290749999999, 12.0092724),
    Addr('Richertsgatan', '2B', 'Göteborg', '412 81', 'Sweden',
         57.6914498, 11.9833941),
    Addr('Brahegatan', '9', 'Göteborg', '415 01', 'Sweden',
         57.730573, 12.0127015),
    Addr('Marconigatan', '7', 'Göteborg', '421 44', 'Sweden',
         57.6519383, 11.9147437),
    Addr('Näverlursgatan', '32', 'Göteborg', '421 44', 'Sweden',
         57.6528971, 11.9105213),
    Addr('Utlandagatan', '24', 'Göteborg', '412 80', 'Sweden',
         57.6872, 11.991266),
    Addr('Gånglåten', '5', 'Göteborg', '421 46', 'Sweden',
         57.6558431, 11.9045289),
    Addr('Studiegången', '6', 'Göteborg', '416 81', 'Sweden',
         57.714335, 12.0377576),
    Addr('Kapellgången', '1', 'Göteborg', '411 30', 'Sweden',
         57.692518, 11.97182),
    Addr('Gibraltargatan', '84', 'Göteborg', '412 79', 'Sweden',
         57.681532, 11.985744),
    Addr('Plejadgatan', '7', 'Göteborg', '417 57', 'Sweden',
         57.704382, 11.93229),
    Addr('Rännvägen', '1', 'Göteborg', '412 58', 'Sweden',
         57.6885252, 11.977216),
    Addr('Stjernsköldsgatan', '14', 'Göteborg', '414 68', 'Sweden',
         57.6856719, 11.926493),
    Addr('Donsögatan', '7', 'Göteborg', '414 74', 'Sweden',
         57.68353, 11.90854),
]


seeder = Seed.seeder()
fake = faker.Faker(locale='sv_SE')

for address in addresses:
    Address.objects.create(
        street_name=address.street_name,
        street_number=address.street_number,
        city=address.city,
        post_code=address.postcode,
        country=address.country,
        latitude=address.lat,
        longitude=address.lng
    )

iter_address = iter(Address.objects.all())

seeder.add_entity(Driver, 3, {
    'name': lambda _: fake.license_plate(),
    'start_address': lambda _: next(iter_address),
})

seeder.add_entity(Stop, 10, {
    'name': lambda _: str(uuid.uuid4()).replace('-', ''),
    'address': lambda _: next(iter_address),
})


def run(*args):
    seeder.execute()

    default_users = [
        ('viren', 'viren@levfinder.se'),
        ('kruslock', 'christoffer@levfinder.se')
    ]

    for user in default_users:
        if not User.objects.filter(username=user[0]):
            u = User(
                username=user[0],
                email=user[1],
                password='levtest123',
            )
            u.is_superuser = True
            u.is_staff = True
            u.save()
