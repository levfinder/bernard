from django.contrib import admin

from bernard.core.models import Driver, Stop, User, Address


admin.site.register(Driver)
admin.site.register(Stop)
admin.site.register(User)
admin.site.register(Address)
