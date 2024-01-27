
from core.models import MyPermission
from core.urls import DApi
from revolver_api.revolver_api.api import Api


@DApi.resource('permission')
class PermissionApi(Api):
    model = MyPermission