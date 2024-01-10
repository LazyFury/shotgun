from django.http import HttpRequest, JsonResponse
from core.api import Rule, Api, validator
from core.route import DApi
from .models import Link, VisitorIP
from core.models import UserModel


@DApi.resource("visitor_ips")
class VisitorIPApi(Api):
    model = VisitorIP

    rules = [
        Rule(name="ip", required=True, message="ip不能为空"),
    ]


class RestApi(Api):
    def auth(self, request: HttpRequest, **kwargs):
        return request.user.is_superuser

    def list(self, request: HttpRequest, **kwargs):
        if self.auth(request=request) is False:
            return JsonResponse(
                {
                    "code": 403,
                    "msg": "无权限",
                }
            )
        return super().list(request, **kwargs)


@DApi.resource("links")
class LinkApi(RestApi):
    model = Link

    rules = [
        Rule(name="url", required=True, message="url不能为空"),
    ]

    @property
    def urls(self):
        return self.get_urls() + [], "link", "link"

    @validator([])
    def list(self, request: HttpRequest, **kwargs):
        return super().list(request, **kwargs)

    @DApi.get("test1", exception_json=True)
    @validator(
        [
            Rule(name="url", required=True, message="url不能为空"),
        ]
    )
    def testReq(self, request: HttpRequest, **kwargs):
        return JsonResponse(
            {
                "method": request.method,
                "params": request.GET,
                "data": request.POST,
            }
        )

    def defaultQuery(self, **kwargs):
        return super().defaultQuery(**kwargs)  # .order_by("-posted_by__is_active")


@DApi.resource("users")
class UserApi(Api):
    model = UserModel

    rules = []

    def pageApi(self, request: HttpRequest, **kwargs):
        return super().pageApi(request, **kwargs)
