# projectManagement/admin.py

from django.contrib import admin
from .models import Board, List, Card
from django.utils.html import format_html

# Inline for Cards in ListAdmin
class CardInline(admin.TabularInline):
    model = Card
    extra = 0
    show_change_link = True
    readonly_fields = ("image_preview",)
    fields = ("title", "status", "start_date", "due_date", "image_preview")

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:40px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Image"

# Inline for Lists in BoardAdmin (and Cards under each List)
class ListInline(admin.TabularInline):
    model = List
    extra = 0
    show_change_link = True

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "status", "budget", "budget_used", "deadline", "start_date", "end_date", "users_list", "managers_list"
    )
    list_filter = ("status", "deadline", "start_date", "end_date")
    search_fields = ("name", "description", "users__username", "managers__username")
    filter_horizontal = ("users", "managers")
    inlines = [ListInline]
    readonly_fields = ()

    def users_list(self, obj):
        return ", ".join([u.username for u in obj.users.all()])
    users_list.short_description = "Users"

    def managers_list(self, obj):
        return ", ".join([u.username for u in obj.managers.all()])
    managers_list.short_description = "Managers"

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "board", "cards_count")
    search_fields = ("name", "board__name")
    list_filter = ("board",)
    inlines = [CardInline]

    def cards_count(self, obj):
        return obj.cards.count()
    cards_count.short_description = "Cards"

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "list", "status", "start_date", "due_date", "assignees_list", "image_preview"
    )
    list_filter = ("status", "start_date", "due_date", "list")
    search_fields = ("title", "description", "list__name", "assignees__username")
    filter_horizontal = ("assignees",)
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:40px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Image"

    def assignees_list(self, obj):
        return ", ".join([u.get_full_name() or u.username for u in obj.assignees.all()])
    assignees_list.short_description = "Assignees"
