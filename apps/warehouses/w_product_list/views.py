from django.views.generic import TemplateView
from django.db.models import Sum
from web_project.template_helpers.theme import TemplateHelper
from web_project import TemplateLayout
from apps.warehouses.models import Warehouse, WarehouseProduct
from web_project.template_tags.theme import has_permission


class WproductListView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        w_products = self.get_annotated_wproducts()
        # Update the context
        context.update(
            {
                "w_products": w_products,
                "w_products_count": WarehouseProduct.objects.count(),
                'has_permission': has_permission
            }
        )
        TemplateHelper.map_context(context)
        return context

    def get_annotated_wproducts(self):
        # Get all warehouses and order them by ID
        return WarehouseProduct.objects.all().order_by('id')
    
