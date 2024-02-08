
from core.models import MyPermission, Post, TableManager
from core.urls import DApi
from revolver_api.revolver_api.api import Api


@DApi.resource('permission')
class PermissionApi(Api):
    model = MyPermission
    
    
@DApi.resource('tableManager')
class TableManagerApi(Api):
    model = TableManager
    
@DApi.resource('articles')
class PostArticle(Api):
    model = Post