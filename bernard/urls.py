from django.contrib import admin
from django.urls import path, include

from bernard.core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bernard.api.urls')),

    path('', views.overview, name='overview'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('vehicles/', views.vehicles, name='vehicles'),
    path('vehicles/<int:id>/', views.vehicle, name='vehicle'),

    path('orders/', views.orders, name='orders'),
    path('orders/<int:id>/', views.order, name='order'),

    path('deliveries/new/', views.deliveries_new, name='deliveries_new'),
]
