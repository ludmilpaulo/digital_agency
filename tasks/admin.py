from django.contrib import admin
from .models import Board, List, Card

class BoardAdmin(admin.ModelAdmin):
    model = Board
    list_display = ('name', 'users_display', 'managers_display', 'budget', 'budget_used', 'start_date', 'end_date', 'status',)
    list_filter = ('name', 'budget', 'budget_used', 'start_date', 'end_date', 'status',)
    search_fields = ('name', 'budget', 'budget_used', 'start_date', 'end_date', 'status',)
    ordering = ('start_date',)

    def users_display(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    users_display.short_description = 'Users'

    def managers_display(self, obj):
        return ", ".join([manager.username for manager in obj.managers.all()])
    managers_display.short_description = 'Managers'
    
class CardAdmin(admin.ModelAdmin):
    model = Card
    list_display = ('title', 'status', 'list',)
    list_filter = ('title',)
    search_fields = ('title', 'list',)
    
class ListAdmin(admin.ModelAdmin):
    model = List
    list_display = ('name', 'board', )
    list_filter = ('name',)
    search_fields = ('name', 'board',)

admin.site.register(Board, BoardAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Card, CardAdmin)
