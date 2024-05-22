from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email', 'date', 'time', 'reason')
    list_filter = ('date', 'time', 'user')
    search_fields = ('user__username', 'phone', 'email', 'reason')
    ordering = ('-date', '-time')

admin.site.register(Appointment, AppointmentAdmin)
