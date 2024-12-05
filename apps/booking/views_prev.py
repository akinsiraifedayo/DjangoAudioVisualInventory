from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.booking.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize
from .forms import *
from apps.clients.forms import *
from apps.warehouses.forms import *
from django.contrib import messages
 from django.urls import reverse_lazy



"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to booking/urls.py file for more pages.
"""


class BookingView(TemplateView):
    form_class = EventForm
    def get_context_data(self, **kwargs):
        if(self.request.POST):
            form = EventForm(self.request.POST)
        else:
            form = EventForm()
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({"form":form})
        # Fetch events from the database
        events = Event.objects.all()

        # Convert events to JavaScript format
        js_events = self.convert_events_to_js(events)

        # Update the context with the events
        context["events"] = js_events

        return context

    def convert_events_to_js(self, events):
        js_events = []
        for event in events:
            if(event.all_day == True):
                all_day= "true"
            else:
                all_day = "false"
            js_event = {
                'id': event.id,
                'url': event.get_url(),
                'title': event.name,
                'start': event.start.timestamp() * 1000,
                'end': event.end.timestamp() * 1000,
                'allDay': all_day,
                'extendedProps': {
                    'calendar': event.event_type
                },
            }
            js_events.append(js_event)
        return js_events


    def post(self, request):
        form = EventForm(self.request.POST)
        if(form.is_valid()):
            instance = form.save()
            return redirect(instance.get_url())
        else:
            context = self.get_context_data()
            context.update({"message": "Your form contains errors!"})
            return render(request, 'app_booking.html', context)


class BookingDetails(TemplateView):
    form_class = EventForm2
    def get_context_data(self, **kwargs):
        event = Event.objects.get(pk=self.kwargs['id'])
        self.request.session['most_recent_event'] = self.kwargs['id']

        clients = Client.objects.all()
        if(self.request.POST):
            form = EventForm2(self.request.POST)
        else:
            form = EventForm2(instance=event)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({"form":form})
        context.update({"event":event})
        context.update({"clients":clients})

        return context

    def post(self, request, *args, **kwargs):
        form = EventForm2(request.POST)
        event = self.get_context_data()["event"]
        if(form.is_valid()):
            event.client = form.cleaned_data['client']
            event.status = form.cleaned_data['status']
            event.save()
            return redirect(event.get_url())
        else:
            context = self.get_context_data()
            context.update({"message": "Your form contains errors!", "form": form})
            return render(request, 'app_booking.html', context)


class EventProductView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        try:
            warehouse = self.kwargs['warehouse']
        except KeyError:
            warehouse = None

        try: 
            event_id = self.request.session.get('most_recent_event')
            event = Event.objects.get(pk=event_id)
        except:
            return redirect(reverse_lazy('events'))
        
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
        context.update({"warehouses": Warehouse.objects.all(), "products": products,"warehouse":warehouse, "selected_warehouse_slug": selected_warehouse_slug, "event": event})

        return context
    
    def post(self, request, *args, **kwargs):
        order = Order.objects.create(
            client=request.user,
            status="Quote",  # Set default status
            order_date=timezone.now()
        )

        form_data = request.POST

        try: 
            event_id = form_data['event_id']
            event = Event.objects.get(pk=event_id)
        except:
            event = None


        # Retrieve submitted product IDs and quantities
        products = [form_data[f'product_id_{i}'] for i in range((len(form_data) - 1) // 2)]
        quantities = [form_data[f'quantity_{i}'] for i in range((len(form_data) - 1) // 2)]

        for product_id, quantity in zip(products, quantities):
            # Create OrderItem and associate it with the order
            product = Product.objects.get(pk=product_id)
            order_item = OrderItem.objects.create(product=product, quantity=quantity)
            order.items.add(order_item)

        # Calculate total amount (assuming each product has a price field)
        total_amount = sum(order_item.product.rental_price * order_item.quantity for order_item in order.items.all())
        order.total_amount = total_amount
        order.event.add(event)
        order.save()

        # Redirect to a success page or another view
        return redirect(reverse_lazy('events'))
    
class ClientFormView(TemplateView):
    template_name = 'add_clients.html'
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = self.form_class()
        context['companies'] = Company.objects.all()  # Add this line to fetch companies
        return context

    def post(self, request, *args, **kwargs):    
        form = self.form_class(request.POST)
        if form.is_valid():
            instance=form.save()
            event = Event.objects.filter(id=self.kwargs.get('id')).first()
            event.client = instance
            event.save()
            messages.success(request, 'client saved')
            return_url = reverse("app-booking-detail", args=[event.id,])
            return redirect(return_url)  # Redirect to the success URL
        else:
            context = self.get_context_data()
            context.update({'form': form},)
            return render(request, self.template_name, context)
        
def BookingDetailsRemove(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        raise Http404("does not exist")
    event.client=None
    event.save()
    return_url = reverse("app-booking-detail", args=[event.id,])
    return redirect(return_url)  # Redirect to the success URL
