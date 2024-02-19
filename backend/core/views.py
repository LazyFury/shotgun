import json
from django.http import HttpRequest
from django.shortcuts import render
from core.libs.wrapper import hasPermission
from core.models import Menu, TableManager, UserToken
from core.urls import api
from plugins.dtk import views as dtk_views
from revolver_api.revolver_api.api import Rule, validator
from revolver_api.revolver_api.response import ApiErrorCode, ApiJsonResponse
from revolver_api.revolver_api.route import Router

from . import api as api_views  # noqa: F401


# Create your views here.
def handler404(request, exception):
    return render(request, "404.html", status=404)


@api.get("test", exception_json=True)
def test(request: HttpRequest):
    def randomStr(length=10):
        import random
        import string

        return "".join(random.sample(string.ascii_letters + string.digits, length))

    return ApiJsonResponse({str(k) + "message": randomStr() for k in range(10)})


@api.get("all", description="所有接口")
def allApi(request: HttpRequest):
    return ApiJsonResponse(
        {"name": "api", "connect": "success", "routers": Router.routes}
    )


def find_device_in_ua_use_regx(ua=""):
    import re

    if re.search("iPhone", ua):
        return "iPhone"
    if re.search("Android", ua):
        return "Android"
    if re.search("Windows Phone", ua):
        return "Windows Phone"
    if re.search("Macintosh", ua):
        return "Macintosh"
    return "PC"


@api.post("login")
@validator(
    [
        Rule("username", required=True, message="用户名不能为空"),
        Rule("password", required=True, message="密码不能为空"),
    ],
    method="post",
)
def login(request: HttpRequest):
    """login


    Args:
        request (HttpRequest): _description_

    Returns:
        _type_: _description_
    """
    try:
        payload = request.valid_data or json.loads(request.body)
    except Exception as e:
        return ApiJsonResponse.error(ApiErrorCode.ERROR, e.__str__())
    # print("payload", payload)
    username = payload.get("username")
    password = payload.get("password")
    try:
        ip = request.META.get("REMOTE_ADDR")
        # print("ip", ip)
        ua = request.META.get("HTTP_USER_AGENT") or ""
        # print("ua", ua)
        is_mobile = ua.find("Mobile") > -1
        # print("is_mobile", is_mobile)
        device = find_device_in_ua_use_regx(ua)
        # print("device", device)
        token = UserToken.get_token(
            username, password, ip=ip, ua=ua, is_mobile=is_mobile, device=device
        )
    except Exception as e:
        return ApiJsonResponse.error(ApiErrorCode.USER_PASSWORD_NOT_MATCH, e.__str__())
    return ApiJsonResponse(
        {
            "token": token.token,
            "expired_at": token.expired_at,
            "user": token.user.to_json(),
        }
    )


@api.post("logout")
def logout(request: HttpRequest):
    UserToken.delete_token(request.user)
    return ApiJsonResponse.success({})


@api.get("profile")
def profile(request: HttpRequest):
    return ApiJsonResponse({"user": request.user.to_json()})

def get_menu_meta(key=""):
    table = TableManager.objects.filter(key=key).first()
    return table.to_json() if table else {}

@api.get("menus")
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
                    "parent": "layout",
                },
            ]
            + [m.to_json() for m in Menu.objects.filter(pid=0)]
            + [
                {
                    "title": "开发人员维护",
                    "icon": "ant-design:code-sandbox",
                    "key": "developer-menu",
                    "children": [
                        # 菜单
                        {
                            "title": "菜单管理",
                            "path": "/system-menu",
                            "key": "system-menu",
                            "component": "TableView",
                            "meta": get_menu_meta("Menus"),
                        },
                        # api 管理
                        {
                            "title": "表格Api管理",
                            "path": "/system-table",
                            "key": "system-table",
                            "component": "dev/SystemTableView",
                            "meta": {
                                "api": "/tableManager",
                                "description": "如果需要使用自动生成的 api 表单，请添加数据后再菜单绑定",
                                "searchForm": {
                                    "fields": [
                                        {
                                            "label": "表格名称",
                                            "name": "title",
                                            "type": "input",
                                            "placeholder": "请输入表格名称",
                                        }
                                    ]
                                },
                                "addForm": {
                                    "fields": [
                                        [
                                            {
                                                "label": "表格名称",
                                                "name": "title",
                                                "type": "input",
                                                "placeholder": "请输入表格名称",
                                                "required": True,
                                                "width": "480px",
                                            },
                                        ],
                                        [
                                            {
                                                "label": "表格描述",
                                                "name": "description",
                                                "type": "input",
                                                "placeholder": "请输入表格描述",
                                                "width": "480px",
                                            },
                                            # key 
                                            {
                                                "label": "唯一Key",
                                                "name": "key",
                                                "type": "input",
                                                "placeholder": "请输入表格Key",
                                                "width": "480px",
                                                "required": True,
                                            },
                                        ],
                                        [
                                            {
                                                "label": "表格API",
                                                "name": "api_url",
                                                "type": "input",
                                                "placeholder": "请输入表格API",
                                                "width": "480px",
                                                "required": True,
                                            },
                                        ],
                                        [
                                            {
                                                "label": "表格列",
                                                "name": "columns",
                                                "type": "textarea",
                                                "placeholder": "请输入表格列",
                                                "width":"100%"
                                            },
                                        ],
                                        [
                                            {
                                                "label": "搜索表单字段",
                                                "name": "search_form_fields",
                                                "type": "textarea",
                                                "placeholder": "请输入搜索表单字段",
                                                "width":"100%"
                                            }
                                        ],[
                                            {
                                                "label": "添加表单字段",
                                                "name": "add_form_fields",
                                                "type": "textarea",
                                                "placeholder": "请输入添加表单字段",
                                                "width":"100%"
                                            }
                                        ]
                                    ]
                                },
                                "table": {
                                    "columns": [
                                        {
                                            "title": "表格名称",
                                            "dataIndex": "title",
                                            "key": "title",
                                            "sortable": True,
                                        },
                                        # description
                                        {
                                            "title": "表格描述",
                                            "dataIndex": "description",
                                            "key": "description",
                                        },
                                        {
                                            "title": "创建时间",
                                            "dataIndex": "create_time",
                                            "key": "created_at",
                                            "sortable": True,
                                        },
                                    ],
                                },
                            },
                        },
                        # 权限
                        {
                            "title": "权限管理",
                            "path": "/system-permission",
                            "key": "system-permission",
                            "component": "TableView",
                            "meta": get_menu_meta("Permissions"),
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


@api.get("dtk")
@hasPermission("dtk_api", allow_superuser=False)
def dtkHandler(request: HttpRequest):
    print("dtkHandler")
    return dtk_views.dataoke(request)
