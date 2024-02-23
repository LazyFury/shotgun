import datetime
from email.policy import default
import json
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from regex import P

from core.libs.utils.time import toUtcTime
from core.libs.utils.upload_to import upload_hash_filename_wrapper
from revolver_api.revolver_api.model import SerializerModel


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
    avatar = models.ImageField(max_length=1000, null=True, blank=True,upload_to=upload_hash_filename_wrapper("avatar",image_field="avatar"))

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
    
    def delete(self, *args, **kwargs):
        if self.is_superuser:
            raise Exception("超级管理员不能删除")
        # super().delete(*args, **kwargs)
        raise Exception("用户不能删除")


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



class UserToken(BaseModel):
    user = models.ForeignKey(
        "core.UserModel", null=True, blank=True, on_delete=models.CASCADE
    )
    token = models.CharField(max_length=100, unique=True)
    expired_at = models.DateTimeField()
    ip = models.CharField(max_length=100, null=True, blank=True)
    device = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    platform = models.CharField(max_length=100, null=True, blank=True)
    is_mobile = models.BooleanField(default=False)
    ua = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.user.username + " -> " + self.token
    
    @staticmethod
    def get_token(username,password,ip="",device="",location="",browser="",platform="",is_mobile=False,ua=""):
        user = UserModel.objects.filter(username=username).first()
        if user is None:
            raise Exception("用户不存在")
        if not user.check_password(password):
            # print("!!!!check_password")
            raise Exception("密码错误")
        # print("!!!!get_token")
        expired = datetime.datetime.now() + datetime.timedelta(days=1)
        token = UserToken.objects.filter(user=user).filter(expired_at__gt=expired).first()
        if token is None:
            token = UserToken()
            token.token = str(uuid.uuid4())
            token.user = user
            token.ip = ip
            token.device = device
            token.ua = ua
            token.expired_at = datetime.datetime.now() + datetime.timedelta(days=1)
            token.save()
        return token

    @staticmethod
    def delete_token(user:UserModel):
        # print("!!!!delete_token")
        tokens = UserToken.objects.filter(user=user).filter(expired_at__gt=datetime.datetime.now())
        for token in tokens:
            token.expired_at = datetime.datetime.now() - datetime.timedelta(days=1)
            token.save()
        
    @staticmethod
    def check_token(token):
        token = UserToken.objects.filter(token=token).first()
        if token is None:
            raise Exception("token不存在")
        expired = datetime.datetime.now()
        print("token.expired_at", token.expired_at)
        print("expired", expired)
        # to unix 
        expired = expired.timestamp()
        expired_at = token.expired_at.timestamp()
        if expired_at < expired:
            return None
        return token.user  
    
    class Meta:
        verbose_name = "用户Token"
        verbose_name_plural = "用户Token"
        
class JSONField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)
    
    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if value is None:
            return value
        return json.loads(value)
    
    def get_prep_value(self, value):
        print("save value", json.dumps(value))
        if value is None:
            return value
        return json.dumps(value)
    
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return json.dumps(value)

class Menu(BaseModel):
    title = models.CharField(max_length=100, null=False, blank=False)
    icon = models.CharField(max_length=100, null=True, blank=True)
    component = models.CharField(max_length=100, null=True, blank=True)
    pid = models.IntegerField(null=True, blank=True,default=0)
    path = models.CharField(max_length=100, null=True, blank=True)
    key = models.CharField(max_length=100, null=True, blank=True)
    meta = models.ForeignKey("core.TableManager",null=True,blank=True,on_delete=models.SET_NULL)
    
    
    def children(self):
        return Menu.objects.filter(pid=self.id).all() or []
    
    def save(self, *args, **kwargs):
        if not self.pid:
            self.pid = 0
        if self.pid == self.id:
            raise Exception("父级菜单不能是自己")
        # todo:在前端设置 defalut value type 并且 format 
        if self.meta_id == "":
            self.meta = None
            self.meta_id = None
        super().save(*args, **kwargs)
    
    def extra_json(self):
        parent = Menu.objects.filter(id=self.pid).first()
        return {
            "children": [menu.to_json() for menu in self.children()],
            "children_count": len(self.children()),
            "has_children": len(self.children()) > 0,
            "parent": parent.key if parent is not None else None,
            "parent_name": parent.title if parent is not None else None,
            "meta":self.meta.to_json() if self.meta is not None else None
        }
        
class TableManager(BaseModel):
    title = models.CharField(max_length=100, null=False, blank=False)
    key = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    api_url = models.CharField(max_length=1000, null=True, blank=True)
    columns = JSONField(max_length=10000, null=True, blank=True)
    search_form_fields = JSONField(max_length=10000, null=True, blank=True)
    add_form_fields = JSONField(max_length=10000, null=True, blank=True)


class Permission(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "权限"
        verbose_name_plural = "权限"
    
    @staticmethod
    def add_model_permission(self,model):
        """ 添加模型权限

        Args:
            model (_type_): _description_
        """
        Permission.objects.create(name=f"create {model}",code=f"create_{model}")
        Permission.objects.create(name=f"read {model}",code=f"read_{model}")
        Permission.objects.create(name=f"update {model}",code=f"update_{model}")
        Permission.objects.create(name=f"delete {model}",code=f"delete_{model}")
        
class UserPermission(BaseModel):
    user = models.ForeignKey(UserModel,null=False,blank=False,on_delete=models.DO_NOTHING)
    permission = models.ForeignKey(Permission,null=False,blank=False,on_delete=models.DO_NOTHING)

class Group(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    permissions = models.ManyToManyField(Permission, blank=True,related_name="core_group_permissions")
    
    
class Post(BaseModel):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    user = models.ForeignKey(
        "core.UserModel", null=True, blank=True, on_delete=models.CASCADE
    )
    
    def extra_json(self):
        user = self.user
        if self.description is None:
            self.description = "-"
        return {
            "user_name": user.username if user is not None else None,
            "sort_title": self.title[:18] + "..." if len(self.title) > 18 else self.title,
            "sort_desc": self.description[:18] + "..." if len(self.description) > 18 else self.description,
        }