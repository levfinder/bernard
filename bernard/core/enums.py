from django.utils.translation import gettext as _

from model_utils import Choices


TRAVEL_MODE = Choices(
    (0, 'driving', _('driving')),
    (1, 'bicycling', _('bicycling'))
)
