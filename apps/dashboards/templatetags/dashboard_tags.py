from django import template
from apps.warehouses.models import *
from apps.booking.models import *
register = template.Library()

@register.filter
def designation_Organisation(designations,organisation):
	return designations.filter(Organisation__Name=organisation)

@register.simple_tag
def get_items_count(items, status):
	return items.filter(status=status).count()


@register.simple_tag
def get_orders_percent(orders, status):
	all = orders.count()
	if(all==0):
		return (0)
	percent = (orders.filter(status=status).count()/ all)*100
	return percent



@register.simple_tag
def rounded(percent):
	percent =round(percent)
	return percent


@register.simple_tag
def geteventwarehouse(event):
	order = Order.objects.filter(event=event).first()
	if(order):
		return order.primary_warehouse.name
	else:
		return ""


@register.simple_tag
def geteventwarehouseloc(event):
	order = Order.objects.filter(event=event).first()
	if(order):
		return order.primary_warehouse.location
	else:
		return ""

@register.simple_tag
def gettrans(warehouse):
	trans = Transfer.objects.filter(fro=warehouse, status="pending")
	return (trans)