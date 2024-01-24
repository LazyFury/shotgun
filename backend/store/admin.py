from django.contrib import admin
from django.utils.html import format_html
from store.models import Product, ProductBrand, ProductCategory, ProductSku, ProductSkuGroup

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','cover', 'price', 'description','categroy','sku_groups')
    search_fields = ('name', 'price', 'description')
    
    def categroy(self,obj):
        return obj.category.name
    
    def sku_groups(self,obj):
        print(obj)
        return ','.join([sku.name for sku in obj.skus.all()])
    
    def cover(self,obj):
        return format_html('<img src="/{}" width="64px" height="64px" />'.format(obj.image))
    
    
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    search_fields = ('name', 'description')
    
@admin.register(ProductSkuGroup)
class ProductSkuGroupAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    search_fields = ('name', 'description')

@admin.register(ProductSku)
class ProductSkuAdmin(admin.ModelAdmin):
    pass
    
@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)