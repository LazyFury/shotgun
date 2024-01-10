from random import choice
from typing import Any
from django.db import models
from backend import settings
from core.models import BaseModel


class VisitorIP(BaseModel):
    ip = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.ForeignKey(
        "link.Link", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.ip

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "短链访客IP记录"
        verbose_name_plural = "短链访客IP记录"

    def to_json(self, **kwargs):
        return self.sample_to_json(related_serializer=False,with_foreign=True)


class QRCode(BaseModel):
    class QRCodeType(models.TextChoices):
        URL = "URL", "超链接"
        TEXT = "TEXT", "文本"

        def __str__(self):
            return self.value

    originUrl = models.URLField(max_length=2000, blank=True, null=True)
    short = models.ForeignKey(
        "link.Link",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    text = models.TextField(blank=True)

    image = models.ImageField(
        null=False,
        blank=True,
        editable=False,
    )

    type = models.CharField(
        choices=QRCodeType.choices,
        max_length=10,
        default=QRCodeType.URL,
        null=False,
        blank=False,
    )
    ip = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "二维码"
        verbose_name_plural = "二维码"



# Create your models here.
class Link(BaseModel):
    """# 短链接

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    STATUS_CHOICES = [("normal", "正常"), ("deleted", "已删除"),("disabled","禁用")]

    url = models.URLField(max_length=2000, unique=True)
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(
        "core.UserModel", null=True, blank=True, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sort_url = models.CharField(max_length=10, blank=True, unique=True)
    
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="normal")

    def __str__(self):
        return self.url

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "短链"
        verbose_name_plural = "短链"

    def save(self, *args, **kwargs):
        if self.sortUrl == "":
            # gen random sore url
            import random
            import string

            letters = string.ascii_letters + string.digits
            self.sortUrl = "".join(random.choice(letters) for i in range(6))
        super(Link, self).save(*args, **kwargs)

    def visitor_ips(self):
        return VisitorIP.objects.filter(link=self)

    def visitor_count(self):
        return self.visitor_ips().count()

    def add_visitor_ip(self, ip):
        VisitorIP.objects.create(ip=ip, link=self)
        
    def to_json(self, *args, **kwargs):
        return super().sample_to_json(with_related=True,with_foreign=True,related_serializer=True)

    def get_status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]

    def extra_json(self):
        qrcode_set = QRCode.objects.filter(short=self).values("image", "text", "type")
        arr =[]
        for qrcode in qrcode_set:
            arr.append(qrcode)
        return {
            "short_url": settings.SITE_URL + "/j/" + self.sort_url,
            "qrcode_set":arr,
            "posted_by__username": self.posted_by.username if self.posted_by is not None else "未知",
            "status_text": self.get_status_display(),
        }
