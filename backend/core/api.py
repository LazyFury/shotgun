
import json
from django.http import HttpRequest
from core.models import DictGroup, Group, Menu, Permission, Post, TableManager, UserModel,DictValue, UserPermission
from core.urls import api
from revolver_api.revolver_api.api import Api, Rule
from revolver_api.revolver_api.response import ApiJsonResponse


@api.resource('permissions')
class PermissionApi(Api):
    model = Permission
    
    
@api.resource('tableManager')
class TableManagerApi(Api):
    model = TableManager

@api.resource("menuManager")
class MenuManagerApi(Api):
    model = Menu
    
    def defaultQuery(self, request):
        return super().defaultQuery(request).filter(pid__isnull=True)
    
@api.resource('articles')
class PostArticle(Api):
    model = Post
    
    rules = [
        Rule("title",message="标题不能为空",required=True),
        Rule("content",message="内容不能为空",required=True),
    ]
    
    
@api.resource('groups')
class GroupApi(Api):
    model = Group
    

@api.resource("users")
class UserApi(Api):
    model = UserModel
    
    public_view = True
    disable_delete = True   
    rules = []

    def pageApi(self, request: HttpRequest, **kwargs):
        return super().pageApi(request, **kwargs)
    
# user-permission 
@api.resource("user-permissions")
class UserPremissions(Api):
    model = UserPermission
    
@api.resource("dict_group")
class DictGroupApi(Api):
    model:DictGroup = DictGroup
    public_view = True
    disable_delete = True
    disable_create = True
    disable_update = True
    rules = []
    
    def get_config(self, request: HttpRequest):
        code = request.GET.get("code")
        group = DictGroup.objects.filter(code=code).first()
        return ApiJsonResponse.success({
            "config":group.get_config() if group else {}
        })
    
    def set_config(self, request: HttpRequest):
        code = request.GET.get("code")
        values = json.loads(request.body.decode("utf-8"))
        group = DictGroup.objects.filter(code=code).first()
        if group:
            try:
                group.set_config(values)
            except Exception as e:
                return ApiJsonResponse.error(str(e))
            return group.get_config()
        return ApiJsonResponse.error("group not found")
    
    def types(self, request: HttpRequest):
        return ApiJsonResponse.success({
            "list":DictValue.types()
        })
    
    def register(self, router, baseUrl="api", middlewares=...):
        router.get(f"{baseUrl}.get_config")(self.get_config)
        router.post(f"{baseUrl}.set_config")(self.set_config)
        router.get(f"{baseUrl}.types")(self.types)
        return super().register(router, baseUrl, middlewares)
    
@api.resource("dict")
class DictApi(Api):
    model = DictValue 
    public_view = True
    disable_delete = True
    disable_create = True
    disable_update = True
    rules = []