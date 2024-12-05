from datetime import date
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.warehouses.models import Warehouse, WarehouseProduct
from apps.warehouses.forms import WarehouseForm, WarehouseProductForm
from django.contrib.auth.mixins import PermissionRequiredMixin

class WproductAddView(PermissionRequiredMixin, TemplateView):
    permission_required = ("w_products.add_w_product")

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        products = WarehouseProduct.objects.all()

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({"products": products})

        return context

    def post(self, request):
        form = WarehouseProductForm(request.POST)
        if form.is_valid():
            if not self.wproduct_exists(form.cleaned_data):
                form.save()
                messages.success(request, 'warehouse product added')
            else:
                messages.error(request, 'warehouse product already exists')
        else:
            messages.error(request, 'adding warehouse product failed')
            print(form.errors)
        return redirect('warehouses')

    def wproduct_exists(self, cleaned_data):
        return Warehouse.objects.filter(
            name__iexact=cleaned_data['name'],
            # products=cleaned_data['products'],
            # location=cleaned_data['location'],
            # contact_person=cleaned_data['contact_person'],
            # contact_email=cleaned_data['contact_email'],
            # contact_phone=cleaned_data['contact_phone']
        ).exists()
