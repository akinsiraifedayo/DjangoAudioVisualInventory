from django.contrib import messages
from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.warehouses.models import Transfer
from django.contrib.auth.mixins import PermissionRequiredMixin
from apps.warehouses.models import Warehouse, Item, WarehouseProduct
from django.shortcuts import redirect, HttpResponse
from django.http import JsonResponse
from apps.inventory.models import Product
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

class TransfersView(PermissionRequiredMixin, TemplateView):
    permission_required = ("w_products.add_w_product")

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        transfers = Transfer.objects.all().order_by('-id')
        warehouses = Warehouse.objects.all()
        warehouses_reversed = list(reversed(warehouses))
        products = Product.objects.all()

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({"transfers": transfers, "warehouses":warehouses, "products":products, "rewarehouses": warehouses_reversed})

        return context






def approve_trans(request):
    pid = request.GET.get('id',None)
    trans = Transfer.objects.filter(id=pid).first()
    ret = trans.make_transfer()
    return HttpResponse(ret)

def reject_trans(request):
    pid = request.GET.get('id',None)
    trans = Transfer.objects.filter(id=pid).first()
    ret = trans.unmake_transfer()
    return HttpResponse(ret)

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@authentication_classes([])
@permission_classes([])
def gettransitems(request):
    pid = request.POST.get('id',None)
    trans = Transfer.objects.filter(id=pid).first()
    ret=[]
    for item in trans.items.all():
        if(item.status != "available"):
            trans.items.remove(item)
        else:
            wareproduct = WarehouseProduct.objects.filter(items__in=[item]).first()
            if(wareproduct not in trans.fro.products.all()):
                trans.items.remove(item)
    trans.save()
    for item in trans.items.all():
        ret.append({"id":item.id, "barcode":item.barcode})
    return JsonResponse({"message":"success","items":ret})


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@authentication_classes([])
@permission_classes([])
def addtransitem(request):
    pid = request.POST.get('trans_id',None)
    barcode = request.POST.get('barcode')
    trans = Transfer.objects.filter(id=pid).first()
    item = Item.objects.filter(barcode=barcode).first()
    if(item == None):
        return JsonResponse({"error":"Item not found!"})
    if(item in trans.items.all()):
        return JsonResponse({"error":"Item already added!"})
    wareproduct = WarehouseProduct.objects.filter(items__in=[item]).first()
    if(wareproduct not in trans.fro.products.all()):
        return JsonResponse({"error":"Item not in warehouse!"})
    if(wareproduct.product != trans.product):
        return JsonResponse({"error":"Item is not the requested product!"})
    if(item.status != "available"):
        return JsonResponse({"error":"Item is not available!"})
    trans.items.add(item)
    trans.save()
    return JsonResponse({"message":"Item successfully added!","id":item.id, "barcode":item.barcode})


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@authentication_classes([])
@permission_classes([])
def removetransitem(request):
    pid = request.POST.get('trans_id',None)
    itemid = request.POST.get('id')
    trans = Transfer.objects.filter(id=pid).first()
    item = Item.objects.filter(id=itemid).first()
    if(item == None):
        return JsonResponse({"error":"Item not found!"})
    if(item not in trans.items.all()):
        return JsonResponse({"error":"Item not added to transfer!"})
    trans.items.remove(item)
    trans.save()
    return JsonResponse({"message":"Item successfully removed!"})