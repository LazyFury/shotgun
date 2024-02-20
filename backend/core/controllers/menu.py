from django.http import HttpRequest
from core.models import Menu, TableManager
from revolver_api.revolver_api.response import ApiJsonResponse
from core.urls import api

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
                                            "name": "title__icontains",
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
                            "component":"dev/systemMonitor"
                        },
                    ],
                },
            ]
        }
    )