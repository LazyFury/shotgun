
from core.models import Group, Menu, Permission, Post, TableManager
from core.urls import api
from revolver_api.revolver_api.api import Api


@api.resource('permissions')
class PermissionApi(Api):
    model = Permission
    
    
@api.resource('tableManager')
class TableManagerApi(Api):
    model = TableManager

@api.resource("menuManager")
class MenuManagerApi(Api):
    model = Menu
    
    def default_query(self, query):
        return super().default_query(query).filter(parent=None)
    
@api.resource('articles')
class PostArticle(Api):
    model = Post
    
    
@api.resource('groups')
class GroupApi(Api):
    model = Group