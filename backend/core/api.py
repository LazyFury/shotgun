from django.http import HttpRequest, JsonResponse
from django.urls import path
from .models import BaseModel


class Api:
    model: BaseModel

    def validate(self, request: HttpRequest, **kwargs):
        print(self.model, "validate")
        return True

    def createApi(self, request: HttpRequest, **kwargs):
        print(self.model, "createApi")
        if self.validate(request, **kwargs) is False:
            return JsonResponse({"error": "validate error"})
        obj = self.model.objects.create(**request.POST.dict())
        return JsonResponse(
            {
                "status": "success",
                "code": 200,
                "data": {
                    "id": obj.pk,
                },
            }
        )

    @property
    def urls(self):
        return (
            [
                path("create", self.createApi, name="getShortUrl"),
            ],
            "api",
            self.__class__.__name__.lower(),
        )
