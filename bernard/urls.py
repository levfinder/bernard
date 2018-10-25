"""bernard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from bernard.core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.overview, name='overview'),

    path('vehicles/', views.vehicles, name='vehicles'),
    path('vehicles/<int:id>/', views.vehicle, name='vehicle'),

    path('orders/', views.orders, name='orders'),
    path('orders/<int:id>/', views.order, name='order'),

    path('deliveries/new', views.deliveries_new, name='deliveries_new'),
]
