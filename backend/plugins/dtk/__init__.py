from revolver_api.revolver_api.route import Router
from .views import dataoke  # noqa: F401


def install(api: Router):
    api.get("dtk", description="大淘客接口")(dataoke)
    print("!!!!install plugin dtk success!!!!")


config = {
    "name": "dataoke",
    "description": "大淘客接口",
    "version": "0.0.1",
    "author": "dtk",
    "email": "",
    "link": "https://www.dataoke.com/",
    "icon":"https://www.dataoke.com/favicon.ico",
    "free":True,
    "price": "0",
    "platform": "all",
    "install": install,
    "requirements":[
        "revolver_api",
        "requests",
        "simple_cache",
        "shotgun",
        "shotgun-core"
    ]
}
