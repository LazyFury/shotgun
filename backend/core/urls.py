

from core.libs.middleware import APIAuthMiddleware
from revolver_api.revolver_api.route import Router


api = Router("api/")
authMiddleware = APIAuthMiddleware("/api", exclude=[
    "/api/login",
    "/api/dtk",
    "/api/groups",
    "/api/test",
    "/api/articles",
    # "/api/menus",
    "/api/system-info",
    "/api/system-monitor",
    "/api/corn"
    ])

urlpatterns = [] + api.urls