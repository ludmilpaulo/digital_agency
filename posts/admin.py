# posts/admin.py

from django.contrib import admin
from .models import Author, Category, Tag, Post, Comment, NewsletterSubscriber
from django.utils.html import format_html

# Inline Comments for Post admin
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("name", "email", "content", "is_approved", "created_date")
    can_delete = True

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "avatar_preview", "linkedin", "twitter")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    readonly_fields = ("avatar_preview",)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.avatar.url)
        return "-"
    avatar_preview.short_description = "Avatar"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    readonly_fields = ()
    def short_description(self, obj):
        return (obj.description[:40] + "...") if obj.description and len(obj.description) > 40 else obj.description
    short_description.short_description = "Description"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "author", "category", "published_date",
        "status", "featured", "newsletter_sent", "views", "created_at", "updated_at", "image_preview"
    )
    list_filter = ("status", "featured", "newsletter_sent", "category", "tags", "created_at", "updated_at")
    search_fields = ("title", "content", "author__user__username", "category__name", "tags__name")
    readonly_fields = ("created_at", "updated_at", "views", "image_preview")
    filter_horizontal = ("tags",)
    inlines = [CommentInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Image"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "name", "email", "is_approved", "created_date", "short_content")
    list_filter = ("is_approved", "created_date", "post")
    search_fields = ("name", "email", "content", "post__title")
    readonly_fields = ("created_date",)

    def short_content(self, obj):
        return (obj.content[:50] + "...") if len(obj.content) > 50 else obj.content
    short_content.short_description = "Content"

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "subscribed_at", "confirmed")
    list_filter = ("confirmed", "subscribed_at")
    search_fields = ("email",)
    readonly_fields = ("subscribed_at",)
