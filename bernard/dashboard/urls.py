from django.urls import path

from bernard.dashboard import views


urlpatterns = [
    path(r'login/', views.login_view, name='login'),
    path(r'logout/', views.logout_view, name='logout'),

    path(r'', views.index, name='index'),
    path(r'drivers/', views.drivers, name='drivers'),
    path(r'stops/', views.stops, name='stops'),
]
