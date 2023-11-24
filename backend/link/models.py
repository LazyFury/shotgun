from multiprocessing import managers
from typing import Any, Self
from django.db import models
from datetime import timedelta, datetime
import uuid
from backend import settings
from config import wx
from core.api import Api
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

    appid = wx.APPID  # testing

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "短链访客IP记录"
        verbose_name_plural = "短链访客IP记录"


class VisitorIPApi(Api):
    model: Any = VisitorIP


# Create your models here.
class Link(models.Model):
    """# 短链接

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """

    url = models.URLField(max_length=2000, unique=True)
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(
        "core.UserModel", null=True, blank=True, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sortUrl = models.CharField(max_length=10, blank=True, unique=True)
    clickCount = models.IntegerField(default=0, editable=False)  # //deprecated

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

    def to_dict(self):
        return {
            "id": self.pk,
            "url": self.url,
            "description": self.description,
            "sortUrl": settings.HOST + "j/" + self.sortUrl,
            "visitorCount": self.visitor_count(),
            "visitorIps": [ip.ip for ip in self.visitor_ips()],
        }


# 微信永久二维码 需要上传一张好友码 群码，超时时间，设置提醒方式
class WXQRCode(models.Model):
    user = models.ForeignKey(
        "core.UserModel", null=False, blank=False, on_delete=models.CASCADE
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    # 二维码类型
    TYPE = (
        (1, "微信好友"),
        (2, "微信群"),
    )
    # 提醒方式
    REMIND = (
        (1, "微信提醒"),
        (2, "邮件提醒"),
    )
    # 二维码
    qrcode = models.ImageField(
        upload_to="%s/qrcode/wx/" % settings.UPLOAD_DIR, null=False, blank=False
    )
    # 二维码类型
    type = models.IntegerField(choices=TYPE, default=1)
    # 超时时间
    timeout = models.DateTimeField(
        default=datetime.now() + timedelta(days=7),  # type: ignore
        help_text="默认 7 天过期",
        blank=True,
        null=True,
    )  # type: ignore # 7天后过期
    # 提醒方式
    remind = models.IntegerField(choices=REMIND, default=1)
    # 二维码描述
    desc = models.CharField(max_length=400, blank=True)
    # 二维码链接
    # link = models.URLField(max_length=2000, blank=True)
    # 二维码状态
    status = models.BooleanField(default=True)
    # 二维码创建时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 二维码更新时间
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.desc

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "微信二维码"
        verbose_name_plural = "微信二维码"


class QRCode(models.Model):
    class QRCodeType(models.TextChoices):
        URL = "URL", "超链接"
        TEXT = "TEXT", "文本"
        WX = "WX", "微信二维码"

        def __str__(self):
            return self.value

    originUrl = models.URLField(max_length=2000, blank=True, null=True)
    short = models.ForeignKey(
        Link,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="short_qrcode_set",
    )
    text = models.TextField(blank=True)

    image = models.ImageField(
        null=False,
        blank=True,
        editable=False,
    )
    wx = models.ForeignKey(
        WXQRCode,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="wx_qrcode_set",
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
