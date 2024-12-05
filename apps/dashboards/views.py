from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.booking.models import *
from datetime import timedelta
from apps.warehouses.models import *


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


class DashboardsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context



class DashboardView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        events = Event.objects.all()
        updelta = timezone.now() - timedelta(days=31)
        up_events = Event.objects.filter(start__lt=updelta)
        event_count = up_events.count()
        up_events = up_events[:10]
        context["event"] = events
        context["on_site"] = Event.objects.filter(status="on_site")
        context["ended"] = Event.objects.filter(status="on_site",end__lte=timezone.now())
        context["ongoing"] = Event.objects.filter(status="on_site",end__gt=timezone.now())
        context["up_events"] = up_events
        context["event_count"] = event_count
        warehouses = Warehouse.objects.all()
        context["warehouses"] = warehouses
        products = WarehouseProduct.objects.none()
        for warehouse in warehouses:
            products = products | warehouse.products.all()
        items = Item.objects.none()
        for product in products:
            items = items | product.items.all()
        context["items"]=items
        context["orders"]= Event.objects.exclude(status="paid")
        return context
