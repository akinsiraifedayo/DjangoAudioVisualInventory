from django.urls import path
from .views import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required


app_name = 'Product'

urlpatterns = [
    path(
        "products/",
        login_required(InventoryView.as_view(template_name="product_inventory1.html")),
        name="products",
    ),
    path(
        "products/<str:warehouse>/",
        login_required(InventoryView.as_view(template_name="product_inventory1.html")),
        name="productsfil",
    ),

    path(
        "products/create/new/",
        login_required(CreateProductView.as_view(template_name="product_create.html")),
        name="products-create",
    ),
    path("products/delete/<str:mid>/", 
        deleteproduct, 
        name="product-delete"
    ),
    path(
        "products/edit/<str:id>/",
        login_required(EditProductView.as_view(template_name="product_create.html")),
        name="product-edit",
    ),
]

