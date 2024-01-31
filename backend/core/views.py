import json
from django.http import HttpRequest
from django.shortcuts import redirect, render
from core.models import UserToken
from core.urls import DApi
from revolver_api.revolver_api.api import Rule, validator
from revolver_api.revolver_api.response import ApiJsonResponse
from revolver_api.revolver_api.route import Router

from . import api as api_views  # noqa: F401


# Create your views here.
def handler404(request, exception):
    return render(request, "404.html", status=404)


@DApi.get("test", exception_json=True)
def test(request: HttpRequest):
    def randomStr(length=10):
        import random
        import string

        return "".join(random.sample(string.ascii_letters + string.digits, length))

    return ApiJsonResponse({str(k) + "message": randomStr() for k in range(10)})


@DApi.get("all", description="所有接口")
def api(request: HttpRequest):
    return ApiJsonResponse(
        {"name": "api", "connect": "success", "routers": Router.routes}
    )

@DApi.post("login")
@validator([
    Rule("username", required=True, message="用户名不能为空"),
    Rule("password", required=True, message="密码不能为空"),
],method="post")
def login(request: HttpRequest):
    try:
        payload = json.loads(request.body)
    except Exception as e:
        return ApiJsonResponse.error(10001, e.__str__())
    username = payload.get("username")
    password = payload.get("password")
    try:
        token = UserToken.get_token(username, password)
    except Exception as e:
        return ApiJsonResponse.error(10001, e.__str__())
    if token is None:
        return ApiJsonResponse.error(10001, "用户名或密码错误")
    return ApiJsonResponse({"token": token.token,"expired_at":token.expired_at, "user": token.user.to_json()})


@DApi.post("logout")
def logout(request: HttpRequest):
    UserToken.delete_token(request.user)
    return ApiJsonResponse.success({})


@DApi.get("menus")
def menus(request: HttpRequest):
    return ApiJsonResponse(
        {
            "menus": [
                {
                    "title": "首页",
                    "icon": "iconoir:apple-shortcuts",
                    "path": "/overview",
                    "key": "overview",
                    "component": "HomeView",
                    "parent":"layout"
                },
                {
                    "title": "用户列表",
                    "path": "/user",
                    "icon": "ant-design:user-outlined",
                    "key": "user",
                    "component": "user/UserView",
                    "meta":{
                        "api":"/users",
                        "description":"处理用户注册、登录、修改密码等操作",
                        "searchForm":{
                            "fields":[
                                {
                                    "label":"用户名",
                                    "name":"username",
                                    "type":"input",
                                    "placeholder":"请输入用户名"
                                },
                                {
                                    "label":"手机号",
                                    "name":"phone",
                                    "type":"input",
                                    "placeholder":"请输入手机号"
                                },
                                {
                                    "label":"邮箱",
                                    "name":"email",
                                    "type":"input",
                                    "placeholder":"请输入邮箱"
                                },
                                # select level
                                {
                                    "label":"用户等级",
                                    "name":"level",
                                    "type":"select",
                                    "placeholder":"请选择用户等级",
                                    "width":"200px",
                                    "options":[
                                        {
                                            "label":"普通用户",
                                            "value":"1"
                                        },
                                        {
                                            "label":"VIP用户",
                                            "value":"2"
                                        },
                                        {
                                            "label":"SVIP用户",
                                            "value":"3"
                                        },
                                    ]
                                },
                            ]
                        },
                        "table":{
                            "batchActions":[
                                {
                                    "label":"批量删除",
                                    "api":"/api/user/delete",
                                    "method":"post",
                                    "confirm":"确定删除选中的用户吗？",
                                    "btnType":"danger",
                                    "action":"delete"
                                }
                            ],
                            "columns":[
                                {
                                    "title":"用户名",
                                    "dataIndex":"username",
                                    "key":"username",
                                    "sortable":True,
                                },
                                {
                                    "title":"邮箱",
                                    "dataIndex":"email",
                                    "key":"email",
                                    "sortable":True,    
                                },
                                {
                                    "title":"创建时间",
                                    "dataIndex":"create_time",
                                    "key":"created_at",
                                    "sortable":True,
                                },
                                {
                                    "title":"操作",
                                    "dataIndex":"action",
                                    "key":"action",
                                    "slots":"action"
                                },
                            ]
                        }
                    }
                },
                {
                    "title": "商品管理",
                    "icon": "iconoir:shopping-bag-pocket",
                    "key": "product-menu",
                    "children": [
                        {
                            "title": "商品列表",
                            "path": "/product",
                            "key": "product",
                            "component": "user/UserView",
                            "meta":{
                                "api":"/products",
                                "description":"处理商品的增删改查等操作",
                                "searchForm":{
                                    "fields":[
                                        {
                                            "label":"商品名称",
                                            "name":"name",
                                            "type":"input",
                                            "placeholder":"请输入商品名称"
                                        },
                                        {
                                            "label":"商品分类",
                                            "name":"category_name",
                                            "type":"select",
                                            "placeholder":"请选择商品分类",
                                            "width":"200px",
                                            "options":[
                                                {
                                                    "label":"普通商品",
                                                    "value":"1"
                                                },
                                                {
                                                    "label":"VIP商品",
                                                    "value":"2"
                                                },
                                                {
                                                    "label":"SVIP商品",
                                                    "value":"3"
                                                },
                                            ]
                                        },
                                    ]
                                },
                                "table":{
                                    "batchActions":[
                                        {
                                            "label":"批量删除",
                                            "api":"/api/product/delete",
                                            "method":"post",
                                            "confirm":"确定删除选中的商品吗？",
                                            "btnType":"danger",
                                        }
                                    ],
                                    "columns":[
                                        {
                                            "title":"商品名称",
                                            "dataIndex":"name",
                                            "key":"name"
                                        },
                                        {
                                            "title":"商品分类",
                                            "dataIndex":"category_name",
                                            "key":"category_name"
                                        },
                                        {
                                            "title":"商品价格",
                                            "dataIndex":"price",
                                            "key":"price"
                                        },
                                        {
                                            "title":"商品库存",
                                            "dataIndex":"stock",
                                            "key":"stock"
                                        },
                                        {
                                            "title":"商品销量",
                                            "dataIndex":"sales",
                                            "key":"sales"
                                        },
                                        {
                                            "title":"商品状态",
                                            "dataIndex":"status",
                                            "key":"status"
                                        },
                                        {
                                            "title":"创建时间",
                                            "dataIndex":"create_time",
                                            "key":"created_at"
                                        },
                                        {
                                            "title":"操作",
                                            "dataIndex":"action",
                                            "key":"action",
                                            "slots":"action"
                                        },
                                    ]
                                }
                            }
                        },
                        {
                            "title": "商品分类",
                            "path": "/product-category",
                            "key": "product-category",
                        },
                        {
                            "title": "商品规格",
                            "path": "/product-sku-group",
                            "key": "product-sku-group",
                        },
                    ],
                },
                {
                    "title": "订单管理",
                    "icon": "ant-design:unordered-list-outlined",
                    "path": "/order",
                    "key": "order",
                },

                {
                    "title": "系统管理",
                    "icon": "ant-design:setting-outlined",
                    "key": "system-menu",
                    "children": [
                        {
                            "title": "系统设置",
                            "path": "/system-setting",
                            "key": "system-setting",
                        },
                        {
                            "title": "角色管理",
                            "path": "/system-role",
                            "key": "system-role",
                        },
                        {
                            "title": "权限管理",
                            "path": "/system-permission",
                            "key": "system-permission",
                            "component": "setting/SystemPermissionView",
                        },
                        # 菜单
                        {
                            "title": "菜单管理",
                            "path": "/system-menu",
                            "key": "system-menu",
                            "component": "setting/SystemMenuView",
                        },
                        {
                            "title": "日志管理",
                            "path": "/system-log",
                            "key": "system-log",
                        },
                        {
                            "title": "系统监控",
                            "path": "/system-monitor",
                            "key": "system-monitor",
                        },
                    ],
                },
            ]
        }
    )
