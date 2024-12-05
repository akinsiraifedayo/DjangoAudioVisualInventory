from django import template
from datetime import datetime
from apps.warehouses.models import *
from apps.booking.models import *


register = template.Library()

@register.simple_tag
def getitemcount(item):
    return (item.w_product.items.first().get_available())

@register.simple_tag
def getitemid(item):
    return (item.w_product.id)

@register.simple_tag
def getitemname(item):
    return (item.w_product.product.name)


@register.simple_tag
def getcount(ccount, inproducts):
    return (ccount + len(inproducts))


@register.simple_tag
def getin_warehouse(product, warehouse):
    wp = warehouse.products.filter(product__id=product.id).first()
    if(not wp):
        return 0
    if(product.item_type== "barcoded"):
        return wp.items.filter(status="available").count()
    else:
        return wp.items.first().get_available()

@register.simple_tag
def getout_warehouse(product, warehouse):
    wp = warehouse.products.filter(product__id=product.id).first()
    if(wp):
        outwp = WarehouseProduct.objects.filter(product__id=product.id).exclude(id=wp.id)
    else:
        outwp = WarehouseProduct.objects.filter(product__id=product.id)
    count = 0
    if(product.item_type== "barcoded"):
        for w in outwp:
            count += w.items.filter(status="available").count()
    else:
        for w in outwp:
            count += w.items.first().get_available()
    return count


@register.simple_tag
def getproducts():
    return Product.objects.all()

@register.filter
def format_currency(value):
    return '{:,.2f}'.format(value)