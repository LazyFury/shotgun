

from revolver_api.revolver_api.route import Router


DApi = Router("v2/api/")

urlpatterns = [] + DApi.urls