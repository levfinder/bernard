from django.conf import settings

from bernard.core.models import SpatialDistance

import googlemaps


gm = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


def get_distance(origin, destination):
    optimise_criteria = 'distance'

    dist = SpatialDistance.objects.filter(
        origin=origin, destination=destination)

    if dist:
        return dist[0].value
    else:
        addresses = [origin, destination]

        coordinates = [(_.latitude, _.longitude) for _ in addresses]
        dist_matrix = gm.distance_matrix(
            origins=coordinates, destinations=coordinates)

        for element_obj, addr_origin in zip(dist_matrix['rows'], addresses):
            elements = element_obj['elements']
            for item, addr_dest in zip(elements, addresses):
                if not addr_origin == addr_dest:
                    SpatialDistance.objects.create(
                        origin=addr_origin,
                        destination=addr_dest,
                        value=item[optimise_criteria]['value'])

        return SpatialDistance.objects.filter(
            origin=origin, destination=destination)


def get_distance_matrix(addresses):
    matrix = []

    for address_origin in addresses:
        row = []
        for address_destination in addresses:
            row.append(get_distance(address_origin, address_destination))
        matrix.append(row)

    return matrix
