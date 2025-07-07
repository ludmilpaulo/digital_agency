# core/admin.py

from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'stars', 'created_at', 'is_active')
    search_fields = ('name', 'role', 'quote')
    list_filter = ('is_active', 'stars')
    ordering = ('-created_at',)
