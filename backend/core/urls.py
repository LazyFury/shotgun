

from core.libs.middleware import APIAuthMiddleware
from revolver_api.revolver_api.route import Router

from plugins import register_plugins  # noqa: F403


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
    "/api/corn",
    "/api/dataoke",
    "/api/plugins"
    ])

# 注册插件
register_plugins(api)

        


urlpatterns = [] + api.urls