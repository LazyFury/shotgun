import datetime
from email.policy import default
import json
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


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

    def convert(self, obj, *args, **kwargs):
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
        belong = UserInviteRelate.objects.filter(user=self).first()
        return {
            "belong_username": belong.belong.username if belong is not None else None,
        }
        
    def fillable(self):
        exclude = ["is_superuser","password"]
        super_fill = super().fillable()
        return [f for f in super_fill if f not in exclude]\
        
    def permissions(self):
        permissions = UserPermission.objects.filter(user=self,enable=True).all()
        return [p.permission.code for p in permissions] + [
            "#","sys"
        ]

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

class DisableDeleteModel(models.Model):
    enable_delete = models.BooleanField(default=False)
    
    def delete(self, *args, **kwargs):
        if not self.enable_delete:
            raise Exception("该数据不允许删除")
        super().delete(*args, **kwargs)
        
    class Meta:
        abstract = True

class Menu(BaseModel):
    title = models.CharField(max_length=100, null=False, blank=False)
    icon = models.CharField(max_length=100, null=True, blank=True)
    component = models.CharField(max_length=100, null=True, blank=True)
    pid = models.IntegerField(null=True, blank=True,default=0)
    path = models.CharField(max_length=100, null=True, blank=True)
    key = models.CharField(max_length=100, null=True, blank=True)
    meta = models.ForeignKey("core.TableManager",null=True,blank=True,on_delete=models.SET_NULL)
    enable_delete = models.BooleanField(default=False)
    enable = models.BooleanField(default=True)
    hidden_on_menu = models.BooleanField(default=False)
    permission_code = models.CharField(max_length=100,null=False,blank=False,default="#")
    
    def children(self):
        return Menu.objects.filter(pid=self.id).all() or []
    
    def save(self, *args, **kwargs):
        if not self.pid:
            self.pid = None
        if self.pid == self.id and self.pid is not None:
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
            "meta":self.meta.to_json() if self.meta is not None else None,
        }
    
    def to_json(self, *args, **kwargs):
        return super().to_json(*args, **kwargs,merge_force=True)
        
    def delete(self, *args, **kwargs):
        if not self.enable_delete:
            raise Exception("该菜单不允许删除")
        super().delete(*args, **kwargs)
        
class TableManager(BaseModel):
    title = models.CharField(max_length=100, null=False, blank=False)
    key = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    api_url = models.CharField(max_length=1000, null=True, blank=True)
    columns = JSONField(max_length=10000, null=True, blank=True)
    search_form_fields = JSONField(max_length=10000, null=True, blank=True)
    add_form_fields = JSONField(max_length=10000, null=True, blank=True)
    enable_delete = models.BooleanField(default=False)
    
    def delete(self, *args, **kwargs):
        if not self.enable_delete:
            raise Exception("该表格不允许删除")
        super().delete(*args, **kwargs)
        


class Permission(BaseModel,DisableDeleteModel):
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
    enable = models.BooleanField(default=True)
    
        
    def extra_json(self):
        return {
            "user_name": self.user.username if self.user is not None else "未知",
            "permission_code": self.permission.code if self.permission is not None else "未知",
            "permission_name": self.permission.name if self.permission is not None else "未知",
        }

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
        
        
        
        
        
        
        
# 系统设置
class DictGroup (BaseModel,DisableDeleteModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    
    def get_config(self):
        dicts = DictValue.objects.filter(group=self)
        config = {}
        for d in dicts:
            if d.type == DictValueType.NUMBER:
                config[d.code] = float(d.value)
            elif d.type == DictValueType.BOOLEAN:
                config[d.code] = str(d.value).lower() != "false" and str(d.value).lower() != "0"
            elif d.type == DictValueType.JSON:
                try:
                    config[d.code] = json.loads(d.value)
                except Exception as e:
                    raise Exception("json 格式错误")
            else:
                config[d.code] = d.value
        return config

    def set_config(self,config):
        for key in config:
            value = config[key]
            d = DictValue.objects.filter(group=self).filter(code=key).first()
            if d is None:
                continue
            d.value = value
            d.save()
    class Meta:
        verbose_name = "字典组"
        verbose_name_plural = "字典组"
        
class DictValueType(models.TextChoices):
    STRING = "string", "字符串"
    NUMBER = "number", "数字"
    BOOLEAN = "boolean", "布尔"
    JSON = "json", "json"
class DictValue(BaseModel,DisableDeleteModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=100, null=False, blank=False)
    type = models.CharField(max_length=100, null=False, blank=False,choices=DictValueType.choices,default=DictValueType.STRING)
    value = models.CharField(max_length=100, null=False, blank=False)
    group = models.ForeignKey(DictGroup,null=True,blank=True,on_delete=models.SET_NULL)

    @staticmethod
    def types():
        return [{
            "label": t[1],
            "value": t[0]
        } for t in DictValueType.choices]
        
    def get_type_display(self):
        return DictValueType(self.type).label
        
    def extra_json(self):
        return {
            "group_name": self.group.name if self.group is not None else "未知",
            "type_name": self.get_type_display(),
        }
    
    def convert(self, obj,key=None):
        if key == "value":
            # try dict value type 
            if self.type == DictValueType.NUMBER:
                return float(obj)
            elif self.type == DictValueType.BOOLEAN:
                return str(obj).lower() != "false" and str(obj).lower() != "0"
            elif self.type == DictValueType.JSON:
                try:
                    return json.loads(obj)
                except Exception as e:
                    raise Exception("json 格式错误")
        return super().convert(obj)
        
    def save(self, *args, **kwargs):
        # value 
        if self.type == DictValueType.NUMBER:
            self.value = str(self.value)
        elif self.type == DictValueType.BOOLEAN:
            self.value = str(self.value).lower() == "true"
        elif self.type == DictValueType.JSON and not isinstance(self.value, str):
            try:
                self.value = json.dumps(self.value)
            except Exception as e:
                raise Exception("json 格式错误")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "字典"
        verbose_name_plural = "字典"