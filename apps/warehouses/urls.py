from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.warehouses.warehouse_list.views import WarehouseListView
from apps.warehouses.warehouse_add.views import WarehouseAddView
from apps.warehouses.warehouse_update.views import WarehouseUpdateView
from apps.warehouses.warehouse_delete.views import WarehouseDeleteView

from apps.warehouses.w_product_list.views import WproductListView
from apps.warehouses.w_product_add.views import WproductAddView
from apps.warehouses.w_product_update.views import WproductUpdateView
from apps.warehouses.w_product_delete.views import WproductDeleteView
from apps.warehouses.warehouse_stock.views import *
from apps.warehouses.transfers.views import *

urlpatterns = [
    path(
        "warehouses/list/",
        login_required(WarehouseListView.as_view(template_name="warehouses_list.html")),
        name="warehouses",
    ),
    path(
        "warehouses/add/",
        login_required(WarehouseAddView.as_view(template_name="warehouses_add.html")),
        name="warehouses-add",
    ),
    path (
        "warehouses/update/<int:pk>",
        login_required(WarehouseUpdateView.as_view(template_name="warehouses_update.html")),
        name="warehouses-update",
    ),
    path (
        "warehouses/stock/edit/<int:pk>",
        login_required(WarehouseStockView.as_view(template_name="warehouses_stock.html")),
        name="warehouses-stock-edit",
    ),
    path (
        "warehouses/delete/<int:pk>/",
        login_required(WarehouseDeleteView.as_view()),
        name="warehouses-delete",
    ),

    path(
        "w_products/list/",
        login_required(WproductListView.as_view(template_name="w_product_list.html")),
        name="w_products",
    ),
    path(
        "w_products/add/",
        login_required(WproductAddView.as_view(template_name="w_product_add.html")),
        name="w_products-add",
    ),
    path (
        "w_products/update/<int:pk>",
        login_required(WproductUpdateView.as_view(template_name="w_product_update.html")),
        name="w_products-update",
    ),
    path (
        "w_products/delete/<int:pk>/",
        login_required(WproductDeleteView.as_view()),
        name="w_products-delete",
    ),
    path (
        "barcode/check",
        login_required(barcodeCheck),
        name="checkbarcode",
    ),
    path (
        "stock/delete/<int:pk>/",
        login_required(StockDeleteView.as_view()),
        name="stock-delete",
    ),
    path (
        "stock/edit/<int:pk>/",
        login_required(StockEditView.as_view()),
        name="stock-edit",
    ),
    path (
        "stock/transfers/",
        login_required(TransfersView.as_view(template_name="transfers.html")),
        name="stock-transfer",
    ),
    path (
        "stock/transfers/accept/",
        login_required(approve_trans),
        name="stock-transfer-accept",
    ),
    path (
        "stock/transfers/reject/",
        login_required(reject_trans),
        name="stock-transfer-reject",
    ),
     path (
        "get/transfers/items/",
        login_required(gettransitems),
        name="get-trans-items",
    ),
    path (
        "add/transfers/item/",
        login_required(addtransitem),
        name="add-trans-item",
    ),
    path (
        "remove/transfers/item/",
        login_required(removetransitem),
        name="remove-trans-item",
    ),

]
