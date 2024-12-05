from django import template
from apps.warehouses.models import *
from apps.inventory.models import *
from datetime import datetime

register = template.Library()

@register.simple_tag
def getstock(product, warehouse):
    p = warehouse.products.filter(product=product).first()
    return (p.stock_quantity())


@register.simple_tag
def getavailable(product, warehouse):
    p = warehouse.products.filter(product=product).first()
    return (p.available_quantity())


@register.simple_tag
def getdamaged(product, warehouse):
    p = warehouse.products.filter(product=product).first()
    return (p.damaged_quantity())


@register.simple_tag
def getreserved(product, warehouse):
    p = warehouse.products.filter(product=product).first()
    return (p.reserved_quantity())

@register.simple_tag
def getitemprice(product, warehouse):
    p = warehouse.products.filter(product=product).first()
    if(p):      
        item = p.items.first()
        if(item):
            return (item.purchase_price)
        else:
            return ("")
    else:
        return ("")
    
@register.simple_tag
def getitemdate(product, warehouse):
    p = warehouse.products.filter(product=product).first()
    if(p):      
        item = p.items.first()
        if(item):
            return (item.purchase_date.strftime("%d/%m/%Y"))
        else:
            return ("")
    else:
        return ("")
    
@register.simple_tag
def getitemstatus(product, warehouse):
    p = warehouse.products.filter(product=product).first()
    if(p):      
        item = p.items.first()
        if(item):
            return (item.status)
        else:
            return ("")
    else:
        return ("")
    

@register.filter
def format_date(date):
    return date.strftime('%Y-%m-%d') if date else ''