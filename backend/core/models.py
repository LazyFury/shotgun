import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from core.libs.utils.time import toUtcTime
from revolver_api.revolver_api.model import SerializerModel
from django.contrib.auth.models import Permission, Group


# Create your models here.
class BaseModel(SerializerModel):
    id = models.AutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, editable=False)

    def convert(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj,datetime.datetime):
            return toUtcTime(obj)
        return super().convert(obj)

    class Meta:
        abstract = True


class UserModel(AbstractUser, BaseModel):
    bio = models.TextField(max_length=500, blank=True)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def extra_json(self):
        return {
            "belong_username": UserInviteRelate.objects.filter(user=self)
            .first()
            .belong.username
            if UserInviteRelate.objects.filter(user=self).first() is not None
            else None,
        }

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserInviteCode(BaseModel):
    code = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(
        "core.UserModel", null=False, blank=False, on_delete=models.CASCADE
    )
    used = models.BooleanField(default=False)

    def __str__(self):
        name = self.user.username if self.user is not None else "未知"
        return name + " -> " + self.code  # type: ignore

    def count(self):
        return UserInviteRelate.objects.filter(invite=self).count()

    class Meta:
        verbose_name = "邀请码"
        verbose_name_plural = "邀请码"


class UserInviteRelate(BaseModel):
    user = models.ForeignKey(
        "core.UserModel", null=True, blank=True, on_delete=models.CASCADE
    )
    invite = models.ForeignKey(
        "core.UserInviteCode", null=True, blank=True, on_delete=models.CASCADE
    )
    belong = models.ForeignKey(
        "core.UserModel",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="belong",
    )
    invite_user_unique_id = models.CharField(
        max_length=10, unique=True, null=False, blank=True
    )

    def __str__(self):
        return self.belong.username + " -> " + self.user.username  # type: ignore

    def save(self, *args, **kwargs):
        if self.belong is None:
            belong = UserModel.objects.filter(pk=self.invite.user.pk).first()  # type: ignore
            if belong is None:
                raise Exception("邀请人不存在")
            self.belong = belong

        if self.user.pk == self.belong.pk:  # type: ignore
            raise Exception("邀请人不能是自己")

        if (
            UserInviteRelate.objects.filter(user=self.belong, belong=self.user).count()
            > 0
        ):
            raise Exception("对方是你的邀请人")

        unique_id = str(self.belong.pk) + "-" + str(self.user.pk)  # type: ignore

        if UserInviteRelate.objects.filter(invite_user_unique_id=unique_id).count() > 0:
            raise Exception("邀请关系已存在")

        if self.invite_user_unique_id is None or self.invite_user_unique_id == "":
            self.invite_user_unique_id = unique_id  # type: ignore

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "邀请关系"
        verbose_name_plural = "邀请关系"


class MyPermission(Permission,BaseModel):
    pass