
from django.http import HttpRequest
from core.models import Group, Menu, Permission, Post, TableManager, UserModel
from core.urls import api
from revolver_api.revolver_api.api import Api, Rule


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
        return super().defaultQuery(request).filter(pid=0)
    
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