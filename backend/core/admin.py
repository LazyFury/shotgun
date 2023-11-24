from django.contrib import admin
from .models import UserModel
from django.contrib.auth.models import Permission

admin.site.site_title = "短链后台管理"
admin.site.site_header = "后台管理"
admin.site.register(Permission)


# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ("username", "uuid", "email", "is_staff", "is_superuser")
