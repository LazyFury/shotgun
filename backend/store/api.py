
from core.urls import DApi
from revolver_api.revolver_api.api import Api
from store.models import Product

# Create your views here.
api = DApi

@api.resource("products")
class ProductApi(Api):
    model = Product
    