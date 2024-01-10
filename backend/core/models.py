import datetime
from logging import warn
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from core.libs.utils.time import toLocalTime


# Create your models here.
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True

    def to_json(self, *args, **kwargs):
        return self.sample_to_json(*args, **kwargs)

    def loop_all_self_attr(
        self, with_foreign=True, with_related=False, related_serializer=False
    ):
        """遍历所有属性

        Returns:
            _type_: _description_
        """
        for key in self.__dict__:
            if hasattr(self, key):
                if key == "_state":
                    continue
                res = getattr(self, key)
                # test type res
                if isinstance(res, datetime.datetime):
                    res = toLocalTime(res)
                yield key, res
        # print(self.foreignKeys())
        for fKey in self.foreignKeys():
            if hasattr(self, fKey.name) and with_foreign is True:
                foreign = getattr(self, fKey.name)
                # print("foreign", fKey.name, foreign)
                # one to one
                if hasattr(foreign, "sample_to_json"):
                    yield (
                        fKey.name,
                        getattr(self, fKey.name).sample_to_json(
                            with_foreign=True,
                            related_serializer=False,
                            with_related=True,
                        ),
                    )
                else:
                    # res = getattr(self, fKey.name) 
                    # yield (
                    #     fKey.name,
                    #     res.__str__() if res is not None else None,
                    # )
                    # 可能是被别的对象引用或者 None ，被别的对象引用的话，这里是一个 RelatedManager 对象,不适合自动处理
                    yield (
                        fKey.name,
                        None
                    )
            # related one to many
            if fKey.related_model is not None and with_related is True:
                related = fKey.related_model
                # print(self.__class__.__name__, fKey.name, related.__class__.__name__)
                arr = []
                if hasattr(related, self.__class__.__name__.lower()) is False:
                    continue

                for item in related.objects.filter(
                    **{self.__class__.__name__.lower(): self}
                ).all():
                    if item is not None and hasattr(item, "sample_to_json"):
                        if related_serializer is True:
                            arr.append(
                                item.sample_to_json(  # type: ignore
                                    with_foreign=False,
                                    related_serializer=False,
                                    with_related=False,
                                )  # type: ignore
                            )
                            continue
                        arr.append(item.__str__())
                yield fKey.name, arr
                yield fKey.name + "_count", len(arr)

    def extra_json(self):
        return {}

    def foreignKeys(self):
        return [f for f in self._meta.get_fields() if f.is_relation]

    def exclude_json_keys(self):
        return [
            "uuid","is_deleted","password"
        ]

    def sample_to_json(
        self,
        with_foreign=True,
        with_related=True,
        related_serializer=False,
        merge_force=False,
    ):
        """转换为json

        Returns:
            _type_: _description_
        """
        result = {
            key: value
            for key, value in self.loop_all_self_attr(
                with_foreign=with_foreign,
                with_related=with_related,
                related_serializer=related_serializer,
            )
        }

        for key, value in self.extra_json().items():
            if merge_force is True:
                result[key] = value
            else:
                if result.get(key) is None:
                    result[key] = value
                else:
                    warn("key %s is exists" % key)
        for key in self.exclude_json_keys():
            if result.keys().__contains__(key):
                del result[key]
        return result


class UserModel(AbstractUser, BaseModel):
    bio = models.TextField(max_length=500, blank=True)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    
    def extra_json(self):
        return {
            "belong_username": UserInviteRelate.objects.filter(user=self).first().belong.username if UserInviteRelate.objects.filter(user=self).first() is not None else None,
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
        return name + " -> " + self.code # type: ignore

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
    invite_user_unique_id = models.CharField(max_length=10, unique=True, null=False, blank=True)

    def __str__(self):
        return self.belong.username + " -> " + self.user.username # type: ignore

    def save(self, *args, **kwargs):
        if self.belong is None:
            belong = UserModel.objects.filter(pk=self.invite.user.pk).first() # type: ignore
            if belong is None:
                raise Exception("邀请人不存在")
            self.belong = belong
        
        if self.user.pk == self.belong.pk: # type: ignore
            raise Exception("邀请人不能是自己")
        
        if UserInviteRelate.objects.filter(user=self.belong, belong=self.user).count() > 0:
            raise Exception("对方是你的邀请人")
        
        unique_id = str(self.belong.pk) + "-" + str(self.user.pk) # type: ignore
        
        if UserInviteRelate.objects.filter(invite_user_unique_id=unique_id).count() > 0:
            raise Exception("邀请关系已存在")
        
        if self.invite_user_unique_id is None or self.invite_user_unique_id == "":
            self.invite_user_unique_id = unique_id # type: ignore
        
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "邀请关系"
        verbose_name_plural = "邀请关系"