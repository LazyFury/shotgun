from django.http import HttpRequest, JsonResponse
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


class Api:
    model: BaseModel

    def validate(self, request: HttpRequest, **kwargs):
        print(self.model, "validate")
        return True

    @preAuth
    def createApi(self, request: HttpRequest, **kwargs):
        print(self.model, "createApi")
        if self.validate(request, **kwargs) is False:
            return JsonResponse({"error": "validate error"})
        obj = self.model.objects.create(**request.POST.dict())
        if obj is None:
            return JsonResponse({"error": "create error"})
        return JsonResponse(
            {
                "status": "success",
                "code": 200,
                "data": obj.to_json(),
            }
        )

    def pageApi(self, request: HttpRequest, **kwargs):
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
        return JsonResponse(
            {
                "status": "success",
                "code": 200,
                "pageable": {
                    "page": page,
                    "size": size,
                    "total": self.model.objects.count(),
                    "totalPage": self.model.objects.count() // size + 1,
                },
                "data": arr,
            }
        )

    def get_one(self, request: HttpRequest, id: int):
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

    @property
    def urls(self):
        return self.get_urls(), "api", "api"

    def get_urls(self):
        return [
            path("create", self.createApi, name="getShortUrl"),
            path("", self.pageApi, name="pageApi"),
            path("<int:id>", self.get_one, name="get_one"),
        ]
