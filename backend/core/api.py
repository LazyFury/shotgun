import enum
from typing import Iterable
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import path
from .models import BaseModel, UserModel


def preAuth(func, role="user"):
    def inner(*args, **kwargs):
        print("preAuth")
        # get request
        req: HttpRequest = None  # type: ignore
        for arg in args:
            if isinstance(arg, HttpRequest):
                req = arg
                break
        if req is None:
            return JsonResponse({"error": "not found request"})
        if req.user.pk is None:
            return JsonResponse({"error": "not normal login"})
        user = UserModel.objects.get(id=req.user.pk)
        if user.is_authenticated is False:
            return JsonResponse({"error": "not login"})
        if user.groups.filter(name=role).exists() is False:
            return JsonResponse({"error": "not auth"})
        return func(*args, **kwargs)

    return inner


class Rule:
    name: str = ""
    required: bool = False
    type: str = "string"
    max_length: int = 0
    min_length: int = 0
    max: int = 0
    min: int = 0
    choices: Iterable = []
    default: str = ""
    message: str = ""
    validator = bool = lambda *args, **kwargs: True

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
            
            
class ApiErrorCode(enum.Enum):
    SUCCESS = 200, "成功"
    ERROR = 400, "失败"
    AUTH_ERROR = 401, "认证失败"
    AUTH_EXPIRED = 402, "认证过期"
    NOT_FOUND = 404, "资源不存在"
    
    USER_NOT_EXIST = 1001, "用户不存在"
    USER_EXIST = 1002, "用户已存在"
    USER_PASSWORD_ERROR = 1003, "密码错误"
    USER_PASSWORD_NOT_MATCH = 1004, "密码不匹配"
    
    USER_NOT_LOGIN = 1005, "用户未登录"
    USER_NOT_AUTH = 1006, "用户未认证"

class ApiJsonResponse(JsonResponse):
    def __init__(self, data, message="", code=ApiErrorCode.SUCCESS,httpCode=200, **kwargs):
        super().__init__(
            {
                "message": message or code.value[1], 
                "code": code.value[0], 
                "data": data
            },
            safe=False,
            json_dumps_params={"ensure_ascii": False, "indent": 0},
            **kwargs,
        )
        self["Access-Control-Allow-Origin"] = "*"
        self["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        self["Access-Control-Max-Age"] = "1000"
        self["Access-Control-Allow-Headers"] = "*"
        self.status_code = httpCode


def def_wrapper(func):
    def inner(*args, **kwargs):
        print("def_wrapper")
        return func(*args, **kwargs)

    return inner


class ApiException(Exception):
    code = 400
    message = "api exception"

apiUrls = []
print("app init")
def Get(url,doc="",authMiddleware=lambda :True):
    print("work on init", doc,url)
    def wrapper(func):
        print("work on wrapper")
        def inner(*args, **kwargs):
            if authMiddleware() is False:
                return JsonResponse({"error": "auth error"})
            print("work on inner")
            return func(*args, **kwargs)
        apiUrls.append(path(url, inner, name=func.__name__))
        return inner
    return wrapper

@Get("api/rr")
def rr(request: HttpRequest):
    return HttpResponse("hello world")

class Api:
    """# 生成API

    Returns:
        _type_: _description_
    """

    model: BaseModel

    rules: Iterable[Rule] = []


    class Validator:
        is_valid = True
        errors = {}

        @property
        def tips(self):
            for key in self.errors:
                return self.errors[key]

        def add_error(self, key, value):
            self.is_valid = False
            self.errors[key] = value

    def validate(self, request: HttpRequest, **kwargs):
        """### 提交数据验证

        Args:
            request (HttpRequest): _description_

        Returns:
            _type_: _description_
        """
        print(self.model, "validate")
        validator = self.Validator()
        for rule in self.rules:
            value = request.POST.get(rule.name)
            if rule.required is True and (value is None or value == ""):
                validator.add_error(
                    rule.name, rule.message if rule.message else "required"
                )
                continue
            if rule.type == "string":
                value = value if value else ""
                if rule.max_length > 0 and len(value) > rule.max_length:
                    validator.add_error(rule.name, f"max_length {rule.max_length}")
                    continue
                if rule.min_length > 0 and len(value) < rule.min_length:
                    validator.add_error(rule.name, f"min_length {rule.min_length}")
                    continue
            if rule.type == "number":
                value = int(value if value else 0)
                if rule.max > 0 and value > rule.max:
                    validator.add_error(rule.name, f"max {rule.max}")
                    continue
                if rule.min > 0 and value < rule.min:
                    validator.add_error(rule.name, f"min {rule.min}")
                    continue
            if rule.type == "choices":
                if value not in rule.choices:
                    validator.add_error(rule.name, f"choices is not in {rule.choices}")
                    continue
            if rule.validator(value) is False:
                validator.add_error(
                    rule.name, rule.message if rule.message else "自定义验证错误"
                )
                continue
        return validator

    def createApi(self, request: HttpRequest, **kwargs):
        """### 创建数据

        Args:
            request (HttpRequest): _description_

        Returns:
            _type_: _description_
        """
        if request.method != "POST":
            return JsonResponse({"error": "only support POST"})
        print(self.model, "createApi")
        validator = self.validate(request, **kwargs)
        if validator.is_valid is False:
            return JsonResponse(
                {
                    "code": 400,
                    "msg": "validate error",
                    "tips": validator.tips if validator.tips else "",
                    "errors": validator.errors,
                }
            )
        try:
            dict = request.POST.dict()
            del dict["id"]
            obj = self.model.objects.create(**dict)
        except Exception as e:
            return JsonResponse({"error": str(e)})
        return JsonResponse(
            {
                "status": "success",
                "code": 200,
                "data": obj.to_json(),
            }
        )

    def updateApi(self, request: HttpRequest, **kwargs):
        """### 更新数据

        Args:
            request (HttpRequest): _description_

        Returns:
            _type_: _description_
        """
        if request.method != "POST":
            return JsonResponse({"error": "only support POST"})
        # print(self.model, "createApi")
        validator = self.validate(request, **kwargs)
        if validator.is_valid is False:
            return JsonResponse(
                {
                    "code": 400,
                    "msg": "validate error",
                    "tips": validator.tips if validator.tips else "",
                    "errors": validator.errors,
                }
            )
        id = request.POST.get("id")
        if id is None or id == "":
            return JsonResponse({"error": "id is required"})
        obj = self.model.objects.filter(pk=id).first()
        if obj is None:
            return JsonResponse({"error": "not found"})
        for key in request.POST.dict():
            setattr(obj, key, request.POST.dict()[key])
        try:
            obj.save()
        except Exception as e:
            return JsonResponse({"error": str(e)})
        return JsonResponse(
            {
                "status": "success",
                "code": 200,
                "msg": "update success",
                "data": obj.to_json(),
            }
        )
        
    def pageApi(self, request: HttpRequest, **kwargs):
        if request.method != "GET":
            return JsonResponse({"error": "only support GET"})
        print(self.model, "pageApi")
        if self.validate(request, **kwargs) is False:
            return JsonResponse({"error": "validate error"})
        page, size = request.GET.get("page", 1), request.GET.get("size", 10)
        page = int(page)
        size = int(size)
        objs = self.model.objects.all().order_by("-id")[
            (page - 1) * size : (page) * size
        ]
        arr = []
        for obj in objs:
            arr.append(obj.to_json())
        return ApiJsonResponse(
            {
                "pageable": {
                    "page": page,
                    "size": size,
                    "total": self.model.objects.count(),
                    "totalPage": self.model.objects.count() // size + 1,
                },
                "list": arr,
            },
            message="获取成功",
        )

    def get_one(self, request: HttpRequest, id: int):
        if request.method != "GET":
            return JsonResponse({"error": "only support GET"})
        print(self.model, "get_one")
        obj = self.model.objects.get(id=id)
        if obj is None:
            return JsonResponse({"error": "not found"})
        return JsonResponse(
            {
                "status": "success",
                "code": 200,
                "data": obj.to_json(),
            }
        )

    def deleteApi(self, request: HttpRequest, id: int):
        if request.method != "DELETE":
            return JsonResponse({"error": "only support DELETE"})
        print(self.model, "deleteApi")
        obj = self.model.objects.get(id=id)
        if obj is None:
            return JsonResponse({"error": "not found"})
        obj.delete()
        return JsonResponse(
            {
                "status": "success",
                "code": 200,
                "data": obj.to_json(),
            }
        )

    @property
    def urls(self):
        return self.get_urls(), "api", self.model.__name__.lower()

    def get_urls(self):
        return [
            path("create", self.createApi, name="getShortUrl"),
            path("", self.pageApi, name="pageApi"),
            path("<int:id>", self.get_one, name="get_one"),
            path("<int:id>/delete", self.deleteApi, name="deleteApi"),
            path("update", self.updateApi, name="updateApi"),
        ]
