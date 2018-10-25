from django.conf.urls import url, include
from rest_framework import routers

from bernard.api import views


router = routers.DefaultRouter()

router.register(r'deliveries', views.DeliveryViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'vehicle', views.VehicleViewSet)
router.register(r'vendor', views.VendorViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
]
