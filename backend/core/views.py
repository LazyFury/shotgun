from django.shortcuts import redirect, render


# Create your views here.
def handler404(request, exception):
    return render(request, "404.html", status=404)


def logout(request):
    from django.contrib.auth import logout

    logout(request)
    return redirect("/")