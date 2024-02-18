
from core.urls import api
from revolver_api.revolver_api.api import Api, Rule
from store.models import Product, ProductCategory

# Create your views here.
api = api

@api.resource("products")
class ProductApi(Api):
    model = Product
    
    public_view = True
    
    rules = [
        Rule("price", message="请填写商品价格！",required=True),
    ]
    
    
@api.resource("product-categories")
class ProductCategoryApi(Api):
    model = ProductCategory