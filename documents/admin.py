# documents/admin.py

from django.contrib import admin
from .models import Document, Signature, OTP, SignatureInvite

# --- Inline for Signatures on the Document page ---
class SignatureInline(admin.TabularInline):
    model = Signature
    extra = 0
    readonly_fields = ("signer", "signature_image", "signed_at", "ip_address", "user_agent", "signature_preview")

    def signature_preview(self, obj):
        if obj.signature_image:
            return f'<img src="{obj.signature_image.url}" style="max-height:60px;"/>'
        return "-"
    signature_preview.short_description = "Preview"
    signature_preview.allow_tags = True

# --- Document Admin ---
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "uploaded_by", "is_signed", "created_at", "file_link", "signed_file_link")
    list_filter = ("is_signed", "created_at", "uploaded_by")
    search_fields = ("title", "uploaded_by__username")
    inlines = [SignatureInline]
    readonly_fields = ("created_at", "file_link", "signed_file_link")

    def file_link(self, obj):
        if obj.file:
            return f'<a href="{obj.file.url}" target="_blank">Download</a>'
        return "-"
    file_link.short_description = "File"
    file_link.allow_tags = True

    def signed_file_link(self, obj):
        if obj.signed_file:
            return f'<a href="{obj.signed_file.url}" target="_blank">Signed File</a>'
        return "-"
    signed_file_link.short_description = "Signed"
    signed_file_link.allow_tags = True

# --- Signature Admin ---
@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "signer", "signed_at", "ip_address", "signature_thumb")
    list_filter = ("signed_at", "signer")
    search_fields = ("document__title", "signer__username", "ip_address")
    readonly_fields = ("signed_at", "signature_thumb")

    def signature_thumb(self, obj):
        if obj.signature_image:
            return f'<img src="{obj.signature_image.url}" style="max-height:60px;"/>'
        return "-"
    signature_thumb.short_description = "Signature"
    signature_thumb.allow_tags = True

# --- OTP Admin ---
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "code", "created_at", "is_still_valid")
    list_filter = ("created_at",)
    search_fields = ("email", "code")
    readonly_fields = ("created_at",)

    def is_still_valid(self, obj):
        return obj.is_valid()
    is_still_valid.boolean = True
    is_still_valid.short_description = "Valid?"

# --- SignatureInvite Admin ---
@admin.register(SignatureInvite)
class SignatureInviteAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "email", "token", "signed", "invited_by", "sent_at", "created_at")
    list_filter = ("signed", "sent_at", "invited_by")
    search_fields = ("document__title", "email", "token")
    readonly_fields = ("token", "created_at", "sent_at")

