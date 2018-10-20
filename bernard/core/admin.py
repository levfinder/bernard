from django.contrib import admin

from bernard.core.models import Delivery, Location, Order, Vendor, Vehicle


admin.site.register(Delivery)
admin.site.register(Location)
admin.site.register(Order)
admin.site.register(Vendor)
admin.site.register(Vehicle)
