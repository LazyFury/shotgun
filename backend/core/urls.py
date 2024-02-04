

from revolver_api.revolver_api.route import Router


DApi = Router("admin_api/")
ClientApi = Router("api/")

urlpatterns = [] + DApi.urls + ClientApi.urls