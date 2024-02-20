import datetime
import json
from os import system
import platform
from time import sleep
from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import render
import psutil
from core.libs.wrapper import hasPermission
from core.urls import api
from plugins.dtk import views as dtk_views
from revolver_api.revolver_api.response import ApiErrorCode, ApiJsonResponse
from revolver_api.revolver_api.route import Router


# api file import
from . import api as api_views  # noqa: F401
from .controllers import *  # noqa: F401,F403


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


@api.get("dtk")
@hasPermission("dtk_api", allow_superuser=False)
def dtkHandler(request: HttpRequest):
    print("dtkHandler")
    return dtk_views.dataoke(request)


@api.get("system-info")
def system_monitor_api(request: HttpRequest):
    return ApiJsonResponse(
        {
            "machine": platform.machine(),
            "platform": platform.platform(),
            "system": platform.system(),
            "version": platform.version(),
            "uname": platform.uname(),
            "name": platform.node(),
            "bootTime": datetime.datetime.fromtimestamp(psutil.boot_time()).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "arch": platform.architecture(),
        }
    )


# sse system monitor
@api.get("system-monitor")
def system_monitor(request: HttpRequest):
    def event_stream():
        while True:
            # cpu rate use python pack
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_rate = f"{cpu_usage}%"
            physical_cpus = psutil.cpu_count(logical=False)
            logical_cpus = psutil.cpu_count(logical=True)
            data = {
                "cpu_rate": cpu_rate,
                "physical_cpus": physical_cpus,
                "logical_cpus": logical_cpus,
                "memory": psutil.virtual_memory().percent,
                "swap": psutil.swap_memory().total / 1024 / 1024 / 1024,
                "memory_GB": psutil.virtual_memory().free / 1024 / 1024 / 1024,
                "memory_all_GB": psutil.virtual_memory().total / 1024 / 1024 / 1024,
                "disk": psutil.disk_usage("/").percent,
                "dist_GB": psutil.disk_usage("/").free / 1024 / 1024 / 1024,
                "dist_all_GB": psutil.disk_usage("/").total / 1024 / 1024 / 1024,
                # "dist_list": psutil.disk_partitions(),
            }
            yield f"data: {json.dumps(data)}\n\n"
            sleep(1)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")


# read all systemctl config
@api.get("corn")
def corn(request: HttpRequest):
    # if linux
    if platform.system() != "Linux":
        return ApiJsonResponse.error(ApiErrorCode.ERROR, "only support linux")
    return ApiJsonResponse({"corn": system("crontab -l")})
