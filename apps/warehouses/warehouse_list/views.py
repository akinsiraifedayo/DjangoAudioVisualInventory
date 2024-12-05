from django.views.generic import TemplateView
from django.db.models import Sum
from web_project.template_helpers.theme import TemplateHelper
from web_project import TemplateLayout
from apps.warehouses.models import Warehouse
from web_project.template_tags.theme import has_permission


class WarehouseListView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        warehouses = self.get_annotated_warehouses()
        # Update the context
        context.update(
            {
                "warehouses": warehouses,
                "warehouses_count": Warehouse.objects.count(),
                'has_permission': has_permission
            }
        )
        TemplateHelper.map_context(context)
        return context

    def get_annotated_warehouses(self):
        # Get all warehouses and order them by ID
        return Warehouse.objects.all().order_by('id')
    
