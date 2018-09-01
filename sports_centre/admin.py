from django.contrib import admin

from .models import Booking, SportsCentre


# Register your models here.
class SportsCentreAdmin(admin.ModelAdmin):
    """Admin page for SportsCentre"""
    search_fields = ['name']
    # list_filter = ['pub_date']
    list_display = ('name', 'opening_time', 'closing_time', 'creator', 'image')


class BookingAdmin(admin.ModelAdmin):
    """Admin page for Booking"""
    search_fields = ['name']
    # list_filter = ['pub_date']
    list_display = ('name', 'sports_centre', 'phone_number', 'date', 'slot')

admin.site.register(SportsCentre, SportsCentreAdmin)
admin.site.register(Booking, BookingAdmin)
