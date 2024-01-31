

from revolver_api.revolver_api.route import Router


DApi = Router("admin_api/")

urlpatterns = [] + DApi.urls