from django.contrib import admin
from .models import Appointment, Rating


@admin.register(Appointment)
class AppoinmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'doctor', 'date', 'time']
    list_filter = ['doctor', ]
    list_per_page = 20
    search_fields = ['doctor', 'name', ]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'stars',]
    list_filter = ['doctor', ]
    search_fields = ['doctor', 'name', ]
    list_per_page = 20
