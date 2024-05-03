from django.contrib import admin

from .models import *

admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(ServiceRequest)


