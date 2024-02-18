
from core.models import Group, Permission, Post, TableManager
from core.urls import api
from revolver_api.revolver_api.api import Api


@api.resource('permission')
class PermissionApi(Api):
    model = Permission
    
    
@api.resource('tableManager')
class TableManagerApi(Api):
    model = TableManager
    
@api.resource('articles')
class PostArticle(Api):
    model = Post
    
    
@api.resource('groups')
class GroupApi(Api):
    model = Group