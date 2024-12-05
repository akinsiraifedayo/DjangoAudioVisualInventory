from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.warehouses.forms import WarehouseForm
from apps.warehouses.models import Warehouse, WarehouseProduct
from django.contrib.auth.mixins import PermissionRequiredMixin

class WarehouseUpdateView(PermissionRequiredMixin, TemplateView):
    permission_required = ("warehouses.update_warehouse")

    def get_context_data(self, **kwargs):
        products = WarehouseProduct.objects.all()

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['warehouse'] = self.get_warehouse(self.kwargs['pk'])
        context.update({"warehouse_products": products})

        return context

    def post(self, request, pk):
        warehouse = self.get_warehouse(pk)
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            if not self.warehouse_exists(form.cleaned_data, warehouse):
                form.save()
                messages.success(request, 'Warehouse Updated')
            else:
                messages.error(request, 'Warehouse Already Exists')
        else:
            messages.error(request, 'Update Failed')
        return redirect('warehouses')

    def get_warehouse(self, pk):
        return Warehouse.objects.get(pk=pk)

    def warehouse_exists(self, cleaned_data, current_warehouse):
        matching_warehouses = Warehouse.objects.filter(
            Q(name__iexact=cleaned_data['name'])
        ).exclude(pk=current_warehouse.pk)
        return matching_warehouses.exists()
