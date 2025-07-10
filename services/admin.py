# services/admin.py

from django.contrib import admin
from .models import Service, Plan, ProposalRequest
import json
from django.utils.html import format_html

# Inline for Plans under Service
class PlanInline(admin.TabularInline):
    model = Plan
    extra = 0
    fields = ("name", "price", "features_pretty", "cta", "popular", "order")
    readonly_fields = ("features_pretty",)

    def features_pretty(self, obj):
        try:
            as_json = json.dumps(obj.features, indent=2)
            return format_html(f'<pre style="white-space: pre-wrap;">{as_json}</pre>')
        except Exception:
            return str(obj.features)
    features_pretty.short_description = "Features"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "icon", "featured", "order")
    search_fields = ("title", "slug", "description")
    list_filter = ("featured",)
    ordering = ("order",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PlanInline]

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "service", "price", "popular", "order", "features_short")
    list_filter = ("popular", "service")
    search_fields = ("name", "service__title", "price")
    ordering = ("service", "order")
    readonly_fields = ("features_pretty",)

    def features_pretty(self, obj):
        try:
            as_json = json.dumps(obj.features, indent=2)
            return format_html(f'<pre style="white-space: pre-wrap;">{as_json}</pre>')
        except Exception:
            return str(obj.features)
    features_pretty.short_description = "Features"

    def features_short(self, obj):
        if isinstance(obj.features, list):
            return ", ".join(obj.features[:3]) + ("..." if len(obj.features) > 3 else "")
        return str(obj.features)
    features_short.short_description = "Features"

@admin.register(ProposalRequest)
class ProposalRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "email", "company", "service", "time_frame", "submitted_at", "short_message"
    )
    search_fields = ("name", "email", "company", "service", "message")
    list_filter = ("submitted_at",)
    readonly_fields = ("submitted_at",)

    def short_message(self, obj):
        return (obj.message[:30] + "...") if len(obj.message) > 30 else obj.message
    short_message.short_description = "Message"
