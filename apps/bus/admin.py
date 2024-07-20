from django.contrib import admin
from .models import Bus, Stop, BusStop, SeatBlock, Booking

# Register your models here.
admin.site.register(Bus)
admin.site.register(Stop)
admin.site.register(BusStop)
admin.site.register(SeatBlock)
admin.site.register(Booking)

