from django.contrib import admin
from django.http.request import HttpRequest
from .models import Link, QRCode, VisitorIP
from django.utils.html import format_html
from .form import QRCodeForm


# Register your models here.
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = [
        "url",
        "description_preview",
        "sortUrl_preview",
        "visitor_count",
        "posted_by",
        "created_at",
        "updated_at",
    ]
    list_per_page = 10
    
    def description_preview(self, obj):
        return obj.description[:16] + "..."

    def sortUrl_preview(self, obj):
        return format_html(
            '<a href="/j/%s" target="_blank">%s</a>'
            % (
                obj.sortUrl,
                obj.sortUrl,
            )
        )


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = [
        "originUrl",
        "image_preview",
        "type_display",
        "ip",
    ]
    form = QRCodeForm
    readonly_fields = ["image", "originUrl", "type", "text", "short", "wx", "ip"]

    def type_display(self, obj: QRCode):
        return QRCode.QRCodeType(obj.type).label

    def image_preview(self, obj: QRCode):
        if obj.image is None:
            return ""
        return format_html(
            '<img src="/%s" width="32px" /><a href="/%s" style="margin-left:10px" target="_blank">查看</a>'
            % (
                obj.image,
                obj.image,
            )
        )

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


@admin.register(VisitorIP)
class VisitorIPAdmin(admin.ModelAdmin):
    list_display = [
        "ip",
        "link",
        "created_at",
    ]
    readonly_fields = ["ip", "link", "created_at"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
