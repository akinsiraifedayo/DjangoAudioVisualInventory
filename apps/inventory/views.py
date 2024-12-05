from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from web_project import TemplateLayout
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.urls import reverse_lazy
from apps.warehouses.models import *
from django.views.decorators.http import require_POST
from django.http import HttpResponse

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""

class InventoryView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        try:
            warehouse = self.kwargs['warehouse']
        except KeyError:
            warehouse = None
        # A function to init the global layout. It is defined in web_project/__init__.py file
        products = Product.objects.all()
        selected_warehouse_slug = None
        if(warehouse != None):
            selected_warehouse_slug = warehouse
            waremodel = Warehouse.objects.filter(slug=warehouse).first()
            wareproducts = waremodel.products.all()
            products = Product.objects.filter(id__in=wareproducts.values_list("product", flat=True))
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        product_count = products.count()
        context['product_count'] = product_count
        context.update({"warehouses": Warehouse.objects.all(), "products": products,"warehouse":warehouse, "selected_warehouse_slug": selected_warehouse_slug})

        return context


class CreateProductView(FormView):
    form_class = ProductForm
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        if(self.request.POST):
            form = ProductForm(self.request.POST)
        else:
            form = ProductForm()
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({"warehouses": Warehouse.objects.all(), "products": Product.objects.all(), "form":form})
        try:
            message = self.request.session["message"]
            del self.request.session["message"]
            context.update({"message":message})
        except KeyError:
            pass
        return context

    def form_valid(self, form, **kwargs):
        obj = form.save(commit=False)
        obj.save()
        form = ProductForm()
        self.request.session["message"] = "saved successfully"
        return HttpResponseRedirect(self.request.path_info)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response



class EditProductView(FormView):
    form_class = ProductForm
    success_url = reverse_lazy('Product:products')

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({"warehouses": Warehouse.objects.all(), "products": Product.objects.all()})
        try:
            message = self.request.session["message"]
            del self.request.session["message"]
            context.update({"message":message})
        except KeyError:
            pass
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Product.objects.get(pk=self.kwargs['id'])
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response



def deleteproduct(request,mid):
    product = Product.objects.filter(id=mid).first()
    product.delete()
    return HttpResponse('success')