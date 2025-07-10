# projects/admin.py

from django.contrib import admin
from .models import Project, ProjectInquiry
from django.utils.html import format_html

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image_preview", "link")
    search_fields = ("title", "description")
    readonly_fields = ("image_preview",)
    list_filter = ("title",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Image"

@admin.register(ProjectInquiry)
class ProjectInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "email", "phone", "company", "project_short", "budget", "submitted_at", "short_message"
    )
    search_fields = ("name", "email", "company", "project", "message")
    list_filter = ("submitted_at", "budget", "company")
    readonly_fields = ("submitted_at",)

    def project_short(self, obj):
        return (obj.project[:30] + "...") if len(obj.project) > 30 else obj.project
    project_short.short_description = "Project"

    def short_message(self, obj):
        return (obj.message[:30] + "...") if len(obj.message) > 30 else obj.message
    short_message.short_description = "Message"
