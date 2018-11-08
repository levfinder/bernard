from django.urls import path

from bernard.dashboard import views


urlpatterns = [
    path(r'login/', views.login_view, name='login'),
    path(r'logout/', views.logout_view, name='logout'),

    path(r'', views.index, name='index'),

    path(r'route/', views.route, name='route'),

    path(r'drivers/', views.drivers, name='drivers'),
    path(r'drivers/new/', views.drivers_new, name='drivers_new'),
    path(r'drivers/<int:_id>/', views.driver, name='driver'),

    path(r'stops/', views.stops, name='stops'),
    path(r'stops/new/', views.stops_new, name='stops_new'),
    path(r'stops/<int:_id>/', views.stop, name='stop'),

    path(r'settings/', views.settings_view, name='settings'),
    path(r'settings/account/', views.settings_account, name='settings_account'),
    path(r'settings/api/', views.settings_api, name='settings_api'),
]
