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

    path('notifications/', views.notifications, name='notifications'),
    path(
        'notifications/new/', views.notification_new, name='notification_new'),
    path('notifications/<int:id>/', views.notification, name='notification'),

    path('tokens/', views.tokens, name='tokens'),
]
