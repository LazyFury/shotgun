from django.http import HttpRequest
from django.shortcuts import redirect, render
from core.urls import DApi
from revolver_api.revolver_api.response import ApiJsonResponse
from revolver_api.revolver_api.route import Router

from . import api

# Create your views here.
def handler404(request, exception):
    return render(request, "404.html", status=404)


def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("/")


@DApi.get("test",exception_json=True)
def test(request: HttpRequest):
    def randomStr(length=10):
        import random
        import string
        return ''.join(random.sample(string.ascii_letters + string.digits, length))
    return ApiJsonResponse({
        str(k) +"message" :randomStr() for k in range(10)
    })
    
    

@DApi.get("all",description="所有接口")
def api(request: HttpRequest):
    return ApiJsonResponse({
        "name": "api",
        "connect": "success",
        "routers":Router.routes
    })
    
@DApi.get("menus")
def menus(request: HttpRequest):
    return ApiJsonResponse({
        "menus":[
            {
                "title":"首页",
                "icon":"iconoir:apple-shortcuts",
                "path":"/overview",
                "key":"overview",
                "component":"HomeView"
            },
            {
                "title":"商品管理",
                "icon":"iconoir:shopping-bag-pocket",
                "key":"product-menu",
                "children":[
                    {
                        "title":"商品列表",
                        "path":"/product",
                        "key":"product",
                        "component":"product/ProductView"
                    },
                    {
                        "title":"商品分类",
                        "path":"/product-category",
                        "key":"product-category"
                    },
                    {
                        "title":"商品规格",
                        "path":"/product-sku-group",
                        "key":"product-sku-group"
                    }
                ]
            },
            {
                "title":"订单管理",
                "icon":"ant-design:unordered-list-outlined",
                "path":"/order",
                "key":"order"
            },
            {
                "title":"用户管理",
                "icon":"ant-design:user-add-outlined",
                "key":"user",
                "children":[
                    {
                        "title":"用户列表",
                        "path":"/user",
                        "key":"user"
                    },
                    {
                        "title":"用户邀请码",
                        "path":"/user-invite-code",
                        "key":"user-invite-code"
                    }
                ]
            },
            {
                "title":"系统管理",
                "icon":"ant-design:setting-outlined",
                "key":"system-menu",
                "children":[
                    {
                        "title":"系统设置",
                        "path":"/system-setting",
                        "key":"system-setting"
                    },
                    {
                        "title":"角色管理",
                        "path":"/system-role",
                        "key":"system-role"
                    },
                    {
                        "title":"权限管理",
                        "path":"/system-permission",
                        "key":"system-permission",
                        "component":"setting/SystemPermissionView"
                    },
                    # 菜单
                    {
                        "title":"菜单管理",
                        "path":"/system-menu",
                        "key":"system-menu",
                        "component":"setting/SystemMenuView"
                    },
                    {
                        "title":"日志管理",
                        "path":"/system-log",
                        "key":"system-log"
                    },
                    {
                        "title":"系统监控",
                        "path":"/system-monitor",
                        "key":"system-monitor"
                    }
                ]
            }
        ]
    })
    