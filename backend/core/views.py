import json
from django.http import HttpRequest
from django.shortcuts import render
from core.libs.wrapper import hasPermission
from core.models import UserToken
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
                {
                    "title": "用户列表",
                    "path": "/user",
                    "icon": "ant-design:user-outlined",
                    "key": "user",
                    "component": "TableView",
                    "meta": {
                        "api": "/users",
                        "description": "处理用户注册、登录、修改密码等操作",
                        "searchForm": {
                            "fields": [
                                {
                                    "label": "用户名",
                                    "name": "username",
                                    "type": "input",
                                    "placeholder": "请输入用户名",
                                },
                                {
                                    "label": "手机号",
                                    "name": "phone",
                                    "type": "input",
                                    "placeholder": "请输入手机号",
                                },
                                {
                                    "label": "邮箱",
                                    "name": "email",
                                    "type": "input",
                                    "placeholder": "请输入邮箱",
                                },
                                # select level
                                {
                                    "label": "用户等级",
                                    "name": "level",
                                    "type": "select",
                                    "placeholder": "请选择用户等级",
                                    "width": "200px",
                                    "options": [
                                        {"label": "普通用户", "value": "1"},
                                        {"label": "VIP用户", "value": "2"},
                                        {"label": "SVIP用户", "value": "3"},
                                    ],
                                },
                            ]
                        },
                        "table": {
                            "columns": [
                                {
                                    "title": "用户名",
                                    "dataIndex": "username",
                                    "key": "username",
                                    "sortable": True,
                                },
                                {
                                    "title": "邮箱",
                                    "dataIndex": "email",
                                    "key": "email",
                                    "sortable": True,
                                },
                                # type 
                                {
                                    "title": "用户等级",
                                    "dataIndex": "id",
                                    "key": "id",
                                    "sortable": True,
                                    "formatter":{
                                        "key":"id",
                                        "mapping_key":"name",
                                        "type":"mapping",
                                        "data":[
                                            {"id":1,"name":"普通用户"},
                                            {"id":2,"name":"VIP用户"},
                                            {"id":3,"name":"SVIP用户"}
                                        ],
                                        "def":"未知"
                                    }
                                },
                                {
                                    "title": "创建时间",
                                    "dataIndex": "create_time",
                                    "key": "created_at",
                                    "sortable": True,
                                },
                                {
                                    "title": "操作",
                                    "dataIndex": "action",
                                    "key": "action",
                                    "slots": "action",
                                },
                            ],
                        },
                    },
                },
                {
                    "title": "文章管理",
                    "icon": "ant-design:file-text-outlined",
                    "key": "article",
                    "path":"/article",
                    "component": "TableView",
                    "meta":{
                        "api":"/articles",
                        "description":"处理文章的增删改查等操作",
                        "searchForm":{
                            "fields":[
                                {
                                    "label":"文章标题",
                                    "name":"title",
                                    "type":"input",
                                    "placeholder":"请输入文章标题",
                                },
                                {
                                    "label":"文章分类",
                                    "name":"category__name",
                                    "type":"select",
                                    "placeholder":"请选择文章分类",
                                    "width":"200px",
                                    "options":[
                                        {"label":"普通文章","value":"1"},
                                        {"label":"VIP文章","value":"2"},
                                        {"label":"SVIP文章","value":"3"},
                                    ],
                                }
                            ]
                        },
                        "addForm":{
                            "fields":[
                                [
                                    {
                                        "label":"文章标题",
                                        "name":"title",
                                        "type":"input",
                                        "placeholder":"请输入文章标题",
                                        "required":True,
                                        "width":"640px",
                                        "suffix":"30字以内"
                                    },
                                ],
                                [
                                    
                                    {
                                        "label":"User",
                                        "name":"user_id",
                                        "type":"select",
                                        "remoteDataApi":"/users",
                                        "props":{
                                            "label":"username",
                                            "value":"id"
                                        },
                                        "placeholder":"请选择作者",
                                        # "required":True,
                                        "width":"240px"
                                    },
                                ],
                                [
                                    {
                                        "label":"文章内容",
                                        "name":"content",
                                        "type":"textarea",
                                        "placeholder":"请输入文章内容",
                                        "required":True,
                                        "width":"640px"
                                    }
                                ]
                            ]
                        },
                        "table":{
                            "columns":[
                                {
                                    "title":"文章标题",
                                    "dataIndex":"sort_title",
                                    "key":"sort_title",
                                    "sortable":True,
                                },
                                {
                                    "title":"Author",
                                    "dataIndex":"user_name",
                                    "key":"user_name",
                                },
                                {
                                    "title":"创建时间",
                                    "dataIndex":"create_time",
                                    "key":"created_at",
                                    "sortable":True,
                                },
                            ],
                        },
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
                            "component": "TableView",
                            "meta": {
                                "name":"商品",
                                "api": "/products",
                                "description": "处理商品的增删改查等操作",
                                "searchForm": {
                                    "fields": [
                                        {
                                            "label": "商品名称",
                                            "name": "name",
                                            "type": "input",
                                            "placeholder": "请输入商品名称",
                                        },
                                        {
                                            "label": "商品分类",
                                            "name": "category__name",
                                            "type": "select",
                                            "placeholder": "请选择商品分类",
                                            "width": "200px",
                                            "options": [
                                                {"label": "普通商品", "value": "1"},
                                                {"label": "VIP商品", "value": "2"},
                                                {"label": "SVIP商品", "value": "3"},
                                            ],
                                        },
                                    ]
                                },
                                "addForm":{
                                    "default":{
                                        "status":True
                                    },
                                    "fields":[
                                        [
                                            {
                                                "label": "商品名称",
                                                "name": "name",
                                                "type": "input",
                                                "placeholder": "请输入商品名称",
                                                "required": True,
                                            },
                                            {
                                                "label": "商品价格",
                                                "name": "price",
                                                "type": "input",
                                                "placeholder": "请输入商品价格",
                                                "required": True,
                                                "suffix":"￥",
                                                "epInputType":"number"
                                            },
                                            {
                                                "label": "商品分类",
                                                "name": "category_id",
                                                "type": "select",
                                                "remoteDataApi":"/product-categories",
                                                "props":{
                                                    "label":"name",
                                                    "value":"id"
                                                },
                                                "placeholder": "请输选择商品分类",
                                                "required": True,
                                                "width":"320px"
                                            },
                                            
                                        ],
                                        [
                                            # status 
                                            {
                                                "label": "商品状态",
                                                "name": "status",
                                                "type": "switch",
                                                "required": True,
                                                "checkedChildren":"上架",
                                                "unCheckedChildren":"下架"
                                            }
                                        ]
                                    ]
                                },
                                "table": {
                                    "pageSize":5,
                                    "columns": [
                                        {
                                            "title": "商品名称",
                                            "dataIndex": "name",
                                            "key": "name",
                                            "className":"font-bold text-lg"
                                        },
                                        {
                                            "title": "商品分类",
                                            "dataIndex": "category_name",
                                            "key": "category_name",
                                            "type":"tag",
                                        },
                                        {
                                            "title": "商品价格",
                                            "dataIndex": "price",
                                            "key": "price",
                                            "className":"font-bold text-lg text-red",
                                            "width":120,
                                            "formatter": {
                                                "type":"number",
                                                "formatStr":"0,0.00",
                                                "prefix":"￥",
                                            }
                                        },
                                        {
                                            "title": "商品状态/上架",
                                            "dataIndex": "status",
                                            "key": "status",
                                            "type":"checkbox",
                                        },
                                        {
                                            "title": "创建时间",
                                            "dataIndex": "create_time",
                                            "key": "created_at",
                                        },
                                        # updated 
                                        {
                                            "title": "更新时间",
                                            "dataIndex": "update_time",
                                            "key": "updated_at",
                                        },
                                    ],
                                    "actions":[
                                        {
                                            "title":"编辑",
                                            "key":"edit",
                                            "type":"primary"
                                        },
                                        {
                                            "title":"删除",
                                            "key":"delete",
                                            "type":"danger"
                                        }
                                    ]
                                },
                            },
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
                # 开发人员维护 group 
                {
                    "title": "开发人员维护",
                    "icon": "ant-design:code-sandbox",
                    "key": "developer-menu",
                    "children": [
                        {
                            "title": "接口管理",
                            "path": "/developer-api",
                            "key": "developer-api",
                            "component": "setting/DeveloperApiView",
                        },
                        {
                            "title": "模型管理",
                            "path": "/developer-model",
                            "key": "developer-model",
                            "component": "setting/DeveloperModelView",
                        },
                        {
                            "title": "插件管理",
                            "path": "/developer-plugin",
                            "key": "developer-plugin",
                            "component": "setting/DeveloperPluginView",
                        },
                    ],
                },
                # table
                {
                    "title": "表格Api管理",
                    "path": "/system-table",
                    "icon": "ant-design:dot-chart-outlined",
                    "key": "system-table",
                    "component":"dev/SystemTableView",
                    "meta": {
                        "api": "/tableManager",
                        "description": "处理表格的增删改查等操作",
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
                                ],
                                [
                                    {
                                        "label": "表格API",
                                        "name": "api_url",
                                        "type": "input",
                                        "placeholder": "请输入表格API",
                                    },
                                    {
                                        "label": "删除API",
                                        "name": "delete_api_url",
                                        "type": "input",
                                        "placeholder": "请输入删除API",
                                    },
                                    {
                                        "label": "创建API",
                                        "name": "create_api_url",
                                        "type": "input",
                                        "placeholder": "请输入创建API",
                                    },
                                    {
                                        "label": "更新API",
                                        "name": "update_api_url",
                                        "type": "input",
                                        "placeholder": "请输入更新API",
                                    },
                                ],
                                [
                                    {
                                        "label": "表格列",
                                        "name": "columns",
                                        "type": "textarea",
                                        "placeholder": "请输入表格列",
                                        "width": "640px",
                                    },
                                ],
                                [
                                    {
                                        "label": "搜索表单字段",
                                        "name": "search_form_fields",
                                        "type": "textarea",
                                        "placeholder": "请输入搜索表单字段",
                                        "width": "540px",
                                    }
                                ],
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
            ]
        }
    )
    
    



@api.get("dtk")
@hasPermission("dtk_api",allow_superuser=False)
def dtkHandler(request: HttpRequest):
    print("dtkHandler")
    return dtk_views.dataoke(request)