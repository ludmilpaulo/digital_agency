from django.contrib import admin
from .models import Service, Plan

class PlanInline(admin.TabularInline):
    model = Plan
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'order']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PlanInline]
    ordering = ["order"]

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'price', 'popular', 'order']
    ordering = ["service", "order"]
