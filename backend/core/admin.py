
import datetime
from django.contrib import admin
from .models import UserInviteCode, UserInviteRelate, UserModel, UserToken
from django.contrib.auth.models import Permission

admin.site.site_title = "短链后台管理"
admin.site.site_header = "后台管理"
admin.site.register(Permission)


app_indexs = (
    ("core", 9),
    ("urlzip", 12),
    ("dtk", -1),
    ("store", 1),
)

def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request, app_label)

        # Sort the apps use app_indexs.
        index_map = {app_label: index for app_label, index in app_indexs}
        app_list = sorted(app_dict.values(), key=lambda x: index_map.get(x["app_label"], 99))

        return app_list
    
admin.AdminSite.get_app_list = get_app_list

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
    
    
@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token","ua","ip","device","expired", "created_at","expired_at")
    list_filter = ("user",)
    search_fields = ("user__username",)
    
    def expired(self, obj):
        expired_at_unix = int(obj.expired_at.timestamp())
        now_unix = int(datetime.datetime.now().timestamp())
        return "有效" if expired_at_unix > now_unix else "过期"