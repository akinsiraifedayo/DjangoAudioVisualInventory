from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q
from django.views.generic import TemplateView, DeleteView
from web_project import TemplateLayout
from apps.inventory.models import *
from apps.warehouses.forms import WarehouseForm
from apps.warehouses.models import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

class WarehouseStockView(PermissionRequiredMixin, TemplateView):
    permission_required = ("w_products.update_w_product")

    def get_context_data(self, **kwargs):
        products = WarehouseProduct.objects.all()
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['warehouse'] = self.get_warehouse(self.kwargs['pk'])
        context['products'] = self.get_products(self.kwargs['pk'])
        context['allProducts']= self.get_unproducts(self.kwargs['pk'])
        context.update({"warehouse_products": products})

        return context

    def post(self, request, pk):
        warehouse = self.get_warehouse(pk)
        pid = request.POST.get("pid")
        barcode = request.POST.get("barcode",None)
        status = request.POST.get("status")
        count = request.POST.get("count")
        purchase_price = request.POST.get("price")
        purchase_date = request.POST.get("date")
        product = get_object_or_404(Product, id=pid)
        wproducts = WarehouseProduct.objects.filter(product=product)

        # Check if the WarehouseProduct already exists for the given product and warehouse
        wp = warehouse.products.filter(product=product).first()

        if wp is None:
            # If WarehouseProduct doesn't exist, create a new one
            wp = WarehouseProduct.objects.create(product=product)
            warehouse.products.add(wp)

        # Create a new Item and associate it with the WarehouseProduct
        if(barcode):
            item = Item(barcode=barcode, status=status, purchase_price=purchase_price, purchase_date=purchase_date)
            item.save()
            wp.items.add(item)
        else:
            items = wp.items.all()
            if(items.count() > 0):
                item = items.first()
                item.count += int(count)
                item.purchase_date = purchase_date
                item.purchase_price = purchase_price
                item.status =status
                item.save()
            else:
                item = Item(count=count, status=status, purchase_price=purchase_price, purchase_date=purchase_date)
                item.save()
                wp.items.add(item)
        wp.save()
        messages.success(request, 'Saved')
        return_url = reverse('warehouses-stock-edit', args=[warehouse.id,])
        return redirect(return_url)

    def get_warehouse(self, pk):
        return Warehouse.objects.get(pk=pk)


    def get_products(self, pk):
        warehouse = self.get_warehouse(pk)
        return warehouse.products.all()

    def get_unproducts(self, pk):
        all_products = Product.objects.all()
        return all_products
        warehouse_products = self.get_products(pk)
        return all_products.exclude(id__in=warehouse_products.values('product__id'))





def barcodeCheck(request):
    barcode = request.GET.get('barcode')
    pid = request.GET.get('id',None)
    mitem=None
    if(pid):
        mitem = Item.objects.filter(id=pid).first()
    if(len(barcode)== 0):
        return HttpResponse("invalid")
    item = Item.objects.filter(barcode=barcode).first()
    if(item == None):
        return HttpResponse("not found")
    elif(item == mitem and mitem):
        return HttpResponse("not found")
    else:
        return HttpResponse("found")


class StockDeleteView(PermissionRequiredMixin, DeleteView):

    permission_required = ("warehouses.delete_stock")

    def get(self, request, pk):
        warehouseP = get_object_or_404(WarehouseProduct, id=pk)
        warehouse = Warehouse.objects.filter(products__in=[warehouseP]).first()
        for item in warehouseP.items.all():
            item.delete()
        warehouseP.delete()
        messages.success(request, 'Stock Deleted')
        url = reverse("warehouses-stock-edit", args=[warehouse.id,])
        return redirect(url)


class StockEditView(PermissionRequiredMixin, TemplateView):
    permission_required = ("w_products.update_w_product")
    template_name = "stock-edit.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        product = self.get_product(self.kwargs['pk'])
        context['product'] = product
        context['warehouse'] = self.get_warehouse(product)

        return context

    def post(self, request, pk):
        mid= request.POST.get("id")
        barcode = request.POST.get("barcode")
        date = request.POST.get("date")
        price = request.POST.get("price")
        status = request.POST.get("status")
        count = request.POST.get("count")
        if(mid):
            item = Item.objects.filter(id=mid).first()
            if(barcode):
                item.barcode=barcode
            if(count):
                item.count=int(count)
            item.status=status
            item.purchase_date =date
            item.purchase_price= float(price)
            item.save()
        else:
            item = Item(barcode=barcode, purchase_date=date, status=status, purchase_price=price)
            item.save()
            wp= WarehouseProduct.objects.filter(id=pk).first()
            wp.items.add(item)
            wp.save()
        url = reverse("stock-edit", args=[pk,])
        return redirect(url)

    def get_product(self, pk):
        return WarehouseProduct.objects.get(pk=pk)

    def get_warehouse(self, product):
        return Warehouse.objects.filter(products__in=[product]).first()

