from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView
from django.contrib import messages
from apps.warehouses.models import Warehouse
from django.contrib.auth.mixins import PermissionRequiredMixin

class WproductDeleteView(PermissionRequiredMixin, DeleteView):

    permission_required = ("w_products.delete_w_product")

    def get(self, request, pk):
        warehouse = get_object_or_404(Warehouse, id=pk)
        warehouse.delete()
        messages.success(request, 'Warehouse Deleted')
        return redirect('warehouses')
