from django.contrib import admin

from bernard.core.models import Delivery, LocationUpdate, Order, Vendor, Vehicle


admin.site.register(Delivery)
admin.site.register(LocationUpdate)
admin.site.register(Order)
admin.site.register(Vendor)
admin.site.register(Vehicle)
