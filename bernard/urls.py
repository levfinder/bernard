from django.contrib import admin
from django.urls import path, include

from bernard.core import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/', include('bernard.core.urls')),
    path('', include('bernard.dashboard.urls')),
]
