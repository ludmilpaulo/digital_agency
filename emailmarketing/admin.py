# emailmarketing/admin.py

from django.contrib import admin
from .models import EmailCampaign, EmailLog
import json
from django.utils.html import format_html

class EmailLogInline(admin.TabularInline):
    model = EmailLog
    extra = 0
    readonly_fields = ('recipient', 'status', 'timestamp', 'opened')
    can_delete = False
    show_change_link = True

@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subject', 'status', 'created_at', 'recipient_count')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'subject', 'recipient_list')
    readonly_fields = ('created_at', 'recipient_pretty')
    inlines = [EmailLogInline]

    def recipient_pretty(self, obj):
        # Pretty print JSON
        try:
            as_json = json.dumps(obj.recipient_list, indent=2)
            return format_html(f'<pre style="white-space: pre-wrap;">{as_json}</pre>')
        except Exception:
            return str(obj.recipient_list)
    recipient_pretty.short_description = "Recipient List (JSON)"

    def recipient_count(self, obj):
        try:
            return len(obj.recipient_list)
        except Exception:
            return '-'
    recipient_count.short_description = "Recipients"

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'campaign', 'recipient', 'status', 'opened', 'timestamp')
    list_filter = ('status', 'opened', 'timestamp')
    search_fields = ('recipient', 'campaign__title')
    readonly_fields = ('timestamp',)

