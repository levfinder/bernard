from django.contrib import admin

from bernard.core.models import Driver, Stop, User, Address, SpatialDistance


admin.site.register(Driver)
admin.site.register(Stop)
admin.site.register(User)
admin.site.register(Address)
admin.site.register(SpatialDistance)
