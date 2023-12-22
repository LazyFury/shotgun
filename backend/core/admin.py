
from django.contrib import admin
from .models import UserInviteCode, UserInviteRelate, UserModel
from django.contrib.auth.models import Permission

admin.site.site_title = "短链后台管理"
admin.site.site_header = "后台管理"
admin.site.register(Permission)


# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ("username", "uuid", "email", "is_staff", "is_superuser")


@admin.register(UserInviteCode)
class UserInviteCodeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "code", "count", "created_at")
    list_filter = ("user",)
    search_fields = ("user__username",)

@admin.register(UserInviteRelate)
class UserInviteRelateAdmin(admin.ModelAdmin):
    list_display = ("code","invite_user_unique_id", "__str__", "user","belong", "created_at")
    list_display_links = ("code", "user","belong")
    list_filter = ("user", "belong","invite")
    # 按时间搜索
    date_hierarchy = "created_at"

    search_fields = ("user__username", "belong__username","invite__code")
    
    def code(self, obj):
        return obj.invite.code