from django.urls import path, include

from bernard.dashboard import views


urlpatterns = [
    path(r'login/', views.login_view, name='login'),
    path(r'logout/', views.logout_view, name='logout'),

    path(r'i18n/', include('django.conf.urls.i18n')),

    path(r'', views.index_view, name='index'),

    path(r'route/', views.route_view, name='route'),

    path(r'drivers/', views.drivers_view, name='drivers'),
    path(r'drivers/new/', views.drivers_new_view, name='drivers_new'),
    path(r'drivers/<int:_id>/', views.driver_view, name='driver'),

    path(r'stops/', views.stops_view, name='stops'),
    path(r'stops/new/', views.stops_new_view, name='stops_new'),
    path(r'stops/<int:_id>/', views.stop_view, name='stop'),

    path(r'settings/', views.settings_view, name='settings'),
    path(r'settings/account/',
         views.settings_account_view, name='settings_account'),
    path(r'settings/api/', views.settings_api_view, name='settings_api'),
]
