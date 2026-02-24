from django.contrib import admin

# Register your models here.
from .models import reservation,Booking,payment

admin.site.register(reservation)
admin.site.register(Booking)
admin.site.register(payment)
