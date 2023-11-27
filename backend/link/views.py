from hashlib import md5
import os
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import qrcode
from backend import settings
from datetime import datetime
from link.models import Link
from .models import QRCode
from ipware import get_client_ip


# Create your views here.
def jump(request: HttpRequest, path: str):
    link = Link.objects.filter(sortUrl=path).first()
    if link is None:
        return render(request, "404.html", status=404)
    else:
        link.clickCount += 1
        client_ip, _ = get_client_ip(request)
        link.add_visitor_ip(client_ip or request.META.get("REMOTE_ADDR"))
        link.save()
    return redirect(link.url)


def qecodeGenerate(request: HttpRequest):
    text = request.GET.get("text") or request.POST.get("text")
    if text is None:
        return render(request, "404.html", status=404)
    else:
        时间目录 = datetime.now().strftime("%y_%m_%d/")
        fileName = md5(text.encode("utf-8")).hexdigest() + ".png"
        dirPath = settings.UPLOAD_DIR + "tmp/qr/" + 时间目录
        if os.path.exists(dirPath) is False:
            os.makedirs(dirPath)
        filePath = dirPath + fileName
        if os.path.exists(filePath) is False:
            QRCode.objects.create(
                image=filePath,
                originUrl=text,
                text=text,
                ip=request.META.get("REMOTE_ADDR"),
            )
            img = qrcode.make(text)
            img.save(filePath)
        file = open(filePath, "rb")
        response = HttpResponse(file)
        file.close()
        response["Content-Type"] = "image/png"
        return response


def genShortUrl(request: HttpRequest):
    url = request.GET.get("url") or request.POST.get("url")
    if url is None:
        return render(request, "404.html", status=404)
    else:
        found = Link.objects.filter(url=url).first()
        if found is not None:
            return JsonResponse(found.to_json())
        short = Link.objects.create(url=url)
        return JsonResponse(short.to_json())


def getShortUrl(request: HttpRequest, pk: int):
    if pk is None:
        return render(request, "404.html", status=404)
    else:
        short = Link.objects.filter(pk=pk).first()
        return JsonResponse(short.to_json() if short is not None else {})


def home(request: HttpRequest):
    if request.method == "POST":
        return genShortUrl(request)
    return render(request, "home.html")


def uploadImage(request: HttpRequest):
    if request.method == "POST":
        file = request.FILES.get("file")
        if file is None:
            return JsonResponse({"code": 400, "msg": "未上传文件"})
        else:
            file_name = file.name
            file_size = file.size
            file_type = file.content_type
            时间目录_下划线 = datetime.now().strftime("%y_%m_%d/")
            file_path = settings.UPLOAD_DIR + 时间目录_下划线 + file_name
            if file_size > 1024 * 1024 * 10:
                return JsonResponse({"code": 400, "msg": "文件过大"})
            if file_type not in ["image/png", "image/jpeg", "image/gif"]:
                return JsonResponse({"code": 400, "msg": "文件格式不支持"})
            if os.path.exists(file_path):
                return JsonResponse({"code": 400, "msg": "文件已存在","path":file_path})
            else:
                with open(file_path, "wb") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                return JsonResponse(
                    {
                        "code": 200,
                        "msg": "上传成功",
                        "data": {
                            "name": file_name,
                            "size": file_size,
                            "type": file_type,
                            "path": file_path,
                        },
                    }
                )
    else:
        return render(request, "uploadImage.html")