from django.contrib import admin
from django.http.request import HttpRequest
from .models import Link, QRCode, VisitorIP
from django.utils.html import format_html
from .form import QRCodeForm


# Register your models here.
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = [
        "url_cut",
        "description_preview",
        "sortUrl_preview",
        "visitor_count",
        "posted_by",
        "created_at",
        "updated_at",
    ]
    list_per_page = 10
    
    def url_cut(self, obj):
        return obj.url[:16] + "..."
    
    def description_preview(self, obj):
        return obj.description[:16] + "..."

    def sortUrl_preview(self, obj):
        return format_html(
            '<a href="/j/%s" target="_blank">%s</a>'
            % (
                obj.sort_url,
                obj.sort_url,
            )
        )

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = [
        "originUrl_cut",
        "image_preview",
        "type_display",
        "ip",
    ]
    form = QRCodeForm
    # readonly_fields = ["image", "originUrl", "type", "text", "short", "wx", "ip"]

    def originUrl_cut(self, obj: QRCode):
        url = obj.originUrl if obj.originUrl is not None else ""
        return url[:32] + "..."

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
        return request.user.is_active


@admin.register(VisitorIP)
class VisitorIPAdmin(admin.ModelAdmin):
    list_display = [
        "ip",
        "link_url_cut",
        "created_at",
    ]
    readonly_fields = ["ip", "link", "created_at"]
    
    def link_url_cut(self, obj):
        return obj.link.url[:16] + "..."

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
