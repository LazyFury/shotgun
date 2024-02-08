from django.db import models
from core.libs.utils.upload_to import upload_hash_filename_wrapper
from core.models import BaseModel





# Create your models here.
class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to=upload_hash_filename_wrapper("product"), null=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey("store.ProductCategory", on_delete=models.CASCADE)
    skus = models.ManyToManyField("store.ProductSkuGroup", blank=True,related_name="products_set")
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def json_key_remark(self):
        return {
            "name":"商品名称",
            "price":"商品价格",
            "image":"商品图片",
            "description":"商品描述",
            "category":"商品分类",
            "skus_set":"商品规格组",
            "status":"商品状态/上架",
            "category_name":"商品分类名称",
            "category_id":"商品分类ID",
            **super().json_key_remark()
        }
    
    def exclude_json_keys(self):
        return super().exclude_json_keys() + ["skus_set"]
    
    def extra_json(self):
        return {
            "category_name":self.category.name,
            "skus":[sku.to_json() for sku in self.skus.all()]
        }

class ProductCategory(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = "商品分类"
        ordering = ["-id"]
        
class ProductSkuGroup(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    products = models.ManyToManyField(Product, blank=True,related_name="skus_set")

    def __str__(self):
        return self.name
    def exclude_json_keys(self):
        return super().exclude_json_keys() + [
            "created_at",
            "updated_at",
            "products",
            "products_set"
        ]
    class Meta:
        verbose_name = "商品规格组"
        verbose_name_plural = "商品规格组"
        ordering = ["-id"]
        
class ProductSku(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    group = models.ForeignKey("ProductSkuGroup", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商品规格"
        verbose_name_plural = "商品规格"
        ordering = ["-id"]

class ProductBrand(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商品品牌"
        verbose_name_plural = "商品品牌"
        ordering = ["-id"]