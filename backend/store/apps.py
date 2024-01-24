from django.apps import AppConfig



class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    verbose_name = "商品管理"
    verbose_name_plural = "商品管理"
    index = 2
    