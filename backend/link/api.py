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

@DApi.resource("links")
class LinkApi(Api):
    model = Link

    rules = [
        Rule(name="url", required=True, message="url不能为空"),
    ]

    @property
    def urls(self):
        return self.get_urls() + [], "link", "link"
    
    @validator([
        Rule(name="url", required=True, message="url不能为空"),
    ])
    def list(self, request: HttpRequest, **kwargs):
        return super().list(request, **kwargs)
    
    @DApi.get("test1",exception_json=True)
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
