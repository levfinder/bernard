from django.contrib import admin

from bernard.core.models import Organisation, User, Notification, Vehicle, \
    LocationUpdate


admin.site.register(Organisation)
admin.site.register(User)
admin.site.register(Notification)
admin.site.register(Vehicle)
admin.site.register(LocationUpdate)
