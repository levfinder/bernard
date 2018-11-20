import googlemaps

from django.conf import settings

from bernard.core.dbapi import get_spatialdistance, create_spatialdistance


gm = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


def get_distance(origin, destination):
    optimise_criteria = 'distance'

    dist = get_spatialdistance(origin=origin, destination=destination)

    if dist:
        return dist.value
    else:
        addresses = [origin, destination]

        coordinates = [(_.latitude, _.longitude) for _ in addresses]
        dist_matrix = gm.distance_matrix(
            origins=coordinates, destinations=coordinates)

        for element_obj, addr_origin in zip(dist_matrix['rows'], addresses):
            elements = element_obj['elements']
            for item, addr_dest in zip(elements, addresses):
                if not get_spatialdistance(
                        origin=addr_origin, destination=addr_dest):
                    create_spatialdistance(
                        origin=addr_origin,
                        destination=addr_dest,
                        value=item[optimise_criteria]['value'])

        return get_spatialdistance(
            origin=origin, destination=destination).value


def get_distance_matrix(addresses):
    matrix = []

    for address_origin in addresses:
        row = []
        for address_destination in addresses:
            row.append(get_distance(address_origin, address_destination))
        matrix.append(row)

    return matrix
