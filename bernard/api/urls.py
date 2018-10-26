from django.conf.urls import url, include
from rest_framework import routers

from bernard.api import views


router = routers.DefaultRouter()

router.register(r'notifications', views.NotificationViewSet)
router.register(r'vehicles', views.VehicleViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
]
