# information/admin.py

from django.contrib import admin
from .models import (
    Image, Carousel, AboutUs, Why_Choose_Us, Team,
    Timeline, Partner, NewsletterSubscriber, Contact
)
from django.utils.html import format_html

# --- Inline for Carousel images ---
class ImageInline(admin.TabularInline):
    model = Carousel.image.through
    extra = 0

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "image_preview")
    readonly_fields = ("image_preview",)
    search_fields = ("image",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "sub_title", "images_count")
    inlines = [ImageInline]
    search_fields = ("title", "sub_title")
    filter_horizontal = ('image',)

    def images_count(self, obj):
        return obj.image.count()
    images_count.short_description = "Image count"

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "born_date", "email", "phone")
    readonly_fields = ("logo_preview", "backgroundImage_preview", "backgroundApp_preview")
    search_fields = ("title", "about", "email", "phone")

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.logo.url)
        return "-"
    logo_preview.short_description = "Logo"

    def backgroundImage_preview(self, obj):
        if obj.backgroundImage:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.backgroundImage.url)
        return "-"
    backgroundImage_preview.short_description = "Background Image"

    def backgroundApp_preview(self, obj):
        if obj.backgroundApp:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.backgroundApp.url)
        return "-"
    backgroundApp_preview.short_description = "Background App"

@admin.register(Why_Choose_Us)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content")
    search_fields = ("title", "content")

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "title", "bio_short", "image_preview", "github", "linkedin")
    search_fields = ("name", "title", "bio")
    readonly_fields = ("image_preview",)

    def bio_short(self, obj):
        return (obj.bio[:50] + "...") if len(obj.bio) > 50 else obj.bio
    bio_short.short_description = "Bio"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Image"

@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ("id", "year", "title", "desc_short")
    search_fields = ("year", "title", "desc")

    def desc_short(self, obj):
        return (obj.desc[:50] + "...") if len(obj.desc) > 50 else obj.desc
    desc_short.short_description = "Description"

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "img_preview", "url")
    search_fields = ("name", "url")
    readonly_fields = ("img_preview",)

    def img_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.img.url)
        return "-"
    img_preview.short_description = "Image"

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "subscribed_at", "is_confirmed")
    list_filter = ("is_confirmed", "subscribed_at")
    search_fields = ("email",)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "from_email", "phone", "timestamp", "short_message")
    list_filter = ("timestamp",)
    search_fields = ("subject", "from_email", "phone", "message")

    def short_message(self, obj):
        return (obj.message[:40] + "...") if len(obj.message) > 40 else obj.message
    short_message.short_description = "Message"
