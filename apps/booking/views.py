from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.booking.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
from .forms import *
from apps.clients.forms import *
from apps.warehouses.forms import *
from apps.warehouses.models import *
from django.contrib import messages
from xhtml2pdf import pisa
import io, json
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

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
                'url': event.get_edit_url(),
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
        event = get_object_or_404(Event, pk=self.kwargs['id'])
        order = Order.objects.filter(event=event).first()
        clients = Client.objects.all()
        warehouses = Warehouse.objects.all()
        t_form = TransferForm()

        # Populate form data based on request method
        form = self.form_class(instance=event)
        if self.request.method == 'GET':
            form = self.form_class(self.request.GET, instance=event)

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = form
        context['t_form'] = t_form
        context['event'] = event
        context['order'] = order
        context['clients'] = clients
        context['warehouses'] = warehouses

        return context


    def post(self, request, *args, **kwargs):
        event = self.get_context_data()["event"]
        item_ids = request.POST.getlist('item_ids')
        if item_ids:
            quantities = request.POST.getlist('quantities')
            for item_id, quantity in zip(item_ids, quantities):
                item = get_object_or_404(OrderItem, id=item_id)
                quantity = int(quantity)
                if quantity == 0:
                    item.delete()
                else:
                    item.quantity = quantity
                    item.save()
            return redirect(event.get_url())
        else:
            form = EventForm2(request.POST)
            if(form.is_valid()):
                verdict = form.update(instance_id=event.id)
                if(verdict == "no quote"):
                    return redirect("event-product-list", event.id)
                return redirect(event.get_url())
            context = self.get_context_data()
            context.update({"message": "Your form contains errors!", "form": form})
            return render(request, 'app_booking.html', context)


class BookingScan(TemplateView):
    def get_context_data(self, **kwargs):
        event = get_object_or_404(Event, pk=self.kwargs['id'])
        order = Order.objects.filter(event=event).first()
        warehouses = Warehouse.objects.all()
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['event'] = event
        context['order'] = order
        context['warehouses'] = warehouses
        if(order.primary_warehouse):
            context['nonwarehouses'] = warehouses.exclude(id=order.primary_warehouse.id)
        else:
            context['nonwarehouses'] = warehouses
        scanned_items = []
        for item in order.scanned_items.all():
            wareproduct = WarehouseProduct.objects.filter(items__in=[item]).first()
            product_name = item.get_product().name
            index = next((i for i, x in enumerate(scanned_items) if x["name"] == product_name), None)
            if index is not None:  # Product name found, increase count
                scanned_items[index]["count"] += 1
            else:
                if(not item.barcode):
                    orderitem = order.items.filter(w_product__items__in=[item]).first()
                    mycount= orderitem.quantity
                else:
                    mycount =1
                scanned_items.append({"id":wareproduct.id,"image":item.get_product().image.url,"name":product_name, "price": item.get_product().rental_price, "count": mycount, "exp_count": order.items.filter(w_product__product__name=product_name).first().quantity, "item_id":item.id})
        context['scanned_items'] = scanned_items
        return context



def removeorderitem(request, id, order_id):
    item = Item.objects.filter(id=id).first()
    order = Order.objects.filter(id=order_id).first()
    orderItem = order.items.filter(w_product__items__in=[item]).first()
    if(not item.barcode and item.count):
        item.unavailable-=orderItem.quantity
        item.save()
    order.scanned_items.remove(item)
    order.save()
    return redirect("scan", order.event.id)


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@authentication_classes([])
@permission_classes([])
def scanitemapi(request):
    order_id = request.POST.get('order_id')
    item_barcode = request.POST.get('barcode')
    order_item_id = request.POST.get('id')
    if(order_item_id != str(0)):
        ttype = "nonbarcoded"
        orderitem = OrderItem.objects.filter(id=order_item_id).first()
        item = orderitem.w_product.items.first()
    else:
        ttype="barcoded"
        item = Item.objects.filter(barcode=item_barcode).first()
    myorder = Order.objects.filter(id=order_id).first()
    if not item:
        return JsonResponse({"error":"Item with barcode does not exist"})
    if(item.status == "reserved"):
        return JsonResponse({"error":"Cannot add a reserved item"})
    if(item.status == "damaged"):
        return JsonResponse({"error":"Cannot add a damaged item"})
    wareproduct = WarehouseProduct.objects.filter(items__in=[item]).first()
    if(wareproduct not in myorder.primary_warehouse.products.all()):
        return JsonResponse({"error":"Item not in event warehouse stock","product_name":wareproduct.product.name, "ttype": wareproduct.product.item_type})
    orders = Order.objects.exclude(Q(event__status="returned") | Q(event__status="ready_to_invoice"))
    order = orders.filter(scanned_items__barcode=item_barcode)
    check = False
    count = 0
    if(ttype == "barcoded"):
        for fitem in wareproduct.items.all():
            if fitem in myorder.scanned_items.all():
                count +=1
                check =True
    if(order.count() ==0 or ttype=="nonbarcoded"):
        product_name = item.get_product().name
        orderItem = myorder.items.filter(w_product__product__name=product_name).first()
        if not orderItem:
            return JsonResponse({"error":"Item cannot be added to this Event"})
        exp_c = orderItem.quantity
        if(ttype == "nonbarcoded"):
            if(item in myorder.scanned_items.all()):
                count = exp_c
        if(count == exp_c):
            return JsonResponse({"error":"Requirement already satisfied"})
        myorder.scanned_items.add(item)
        item.unavailable+=exp_c
        item.save()
        myorder.save()
        if not check:
            if(ttype == "barcoded"):
                mycount =1
            else:
                mycount = exp_c
            return JsonResponse({"id":wareproduct.id,"image":item.get_product().image.url,"name":product_name, "price": item.get_product().rental_price, "count": mycount, "exp_count": myorder.items.filter(w_product__product__name=product_name).first().quantity, "item_id":item.id})
        else:
            return JsonResponse({"id":wareproduct.id,"count":count+1,"status":"success","exp_count": myorder.items.filter(w_product__product__name=product_name).first().quantity, "item_id":item.id})
    else:
        return JsonResponse({"error":"Item not available or being used in another event"})


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@authentication_classes([])
@permission_classes([])
def transitemapi(request):
    request_json = None
    try:
        # accept data from api
        request_json = json.loads(request.body.decode('utf-8'))
        ware_id = request_json.get('ware_id')
        item_barcode = request_json.get('barcode')
        warep_id = request_json.get('warep_id')
        count = int(request_json.get('count'))
    except:
        # accept data from form
        ware_id = request.POST.get('ware_id')
        item_barcode = request.POST.get('barcode')
        warep_id = request.POST.get('warep_id')
        count = int(request.POST.get('count'))

    to = Warehouse.objects.filter(id=ware_id).first()
    if(not to):
        return JsonResponse({"error":"Event warehouse not set"})
    item = Item.objects.filter(barcode=item_barcode).first()
    if(warep_id != 0 and warep_id != None):
        item = WarehouseProduct.objects.filter(id=warep_id).first().items.first()
        if request_json:
            fro = request_json.get('fro_id')
        else:
            fro = request.POST.get('fro_id')
        
        fro = Warehouse.objects.filter(id=fro).first() 
    else:
        frop = WarehouseProduct.objects.filter(items__in=[item]).first()
        fro = Warehouse.objects.filter(products__in=[frop]).first()
    if(not to):
        return JsonResponse({"error":"Could not get item warehouse"})
    trans = Transfer(fro=fro,to=to,item=item)
    if(count !=0):
        trans.count=count
    trans.save()
    return JsonResponse({"message":"Request successfully sent!"})



class EventProductView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        event = get_object_or_404(Event, id=self.kwargs['event'])
        order = Order.objects.filter(event=event).first()
        # A function to init the global layout. It is defined in web_project/__init__.py file
        products = WarehouseProduct.objects.all()
        selected_warehouse_slug = None
        warehouse = None
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        product_count = products.count()
        context['product_count'] = product_count
        context.update({"warehouses": Warehouse.objects.all(), "products": products,"warehouse":warehouse, "selected_warehouse_slug": selected_warehouse_slug, "event":event,})

        return context

    def dispatch(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=self.kwargs['event'])
        order = Order.objects.filter(event=event).first()
        if order and order.primary_warehouse:
            return redirect(reverse("eventproductsfil", kwargs={'event': event.id, 'warehouse': order.primary_warehouse.id}))
        return super().dispatch(request, *args, **kwargs)



def getin_warehouse(product, warehouse):
    wp = warehouse.products.filter(product__id=product.id).first()
    if(not wp):
        return 0
    if(product.item_type== "barcoded"):
        return wp.items.filter(status="available").count()
    else:
        return wp.items.first().get_available()

def getout_warehouse(product, warehouse):
    wp = warehouse.products.filter(product__id=product.id).first()
    if(wp):
        outwp = WarehouseProduct.objects.filter(product__id=product.id).exclude(id=wp.id)
    else:
        outwp = WarehouseProduct.objects.filter(product__id=product.id)
    count = 0
    if(product.item_type== "barcoded"):
        for w in outwp:
            count += w.items.filter(status="available").count()
    else:
        for w in outwp:
            count += w.items.first().get_available()
    return count


def removequoteitem(request, item_id, order_id):
    item = OrderItem.objects.filter(id=item_id).first()
    item.delete()
    order = Order.objects.filter(id=order_id).first()
    return redirect("eventproductsfil", order.event.id, order.primary_warehouse.id)

def changetohold(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    event= order.event
    order.status ="hold"
    event.status="hold"
    order.save()
    event.save()
    return redirect("scan", order.event.id)

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@authentication_classes([])
@permission_classes([])
def additemtoquote(request):
    order_id = request.POST.get('order_id')
    product_id = request.POST.get('product_id')
    count = request.POST.get('count')
    order = Order.objects.filter(id=order_id).first()
    product = Product.objects.filter(id=product_id).first()
    mywarehouse = order.primary_warehouse
    wp = mywarehouse.products.filter(product=product).first()
    print(product)
    if(wp == None):
        wp = WarehouseProduct(product=product)
        wp.save()
        mywarehouse.products.add(wp)
        mywarehouse.save()
    orderitem = order.items.filter(w_product=wp).first()
    if(orderitem==None):
        orderitem = OrderItem(w_product=wp, quantity=count)
        orderitem.save()
        order.items.add(orderitem)
        order.save()
        message = "Product added successfully"
    else:
        orderitem.quantity=count
        orderitem.save()
        message = "Product edited successfully"
    data ={
        "id":product.id,
        "image": product.image.url,
        "name" : product.name,
        "manufacturer": product.manufacturer,
        "inn": getin_warehouse(product, mywarehouse),
        "out": getout_warehouse(product, mywarehouse),
        "quantity":count,
        "remove": orderitem.get_remove_url()
    }
    return JsonResponse({"message":message, "data":data})

class EventProductWareView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        event = get_object_or_404(Event, id=self.kwargs['event'])
        warehouse = get_object_or_404(Warehouse, id=self.kwargs['warehouse'])
        order = Order.objects.filter(event=event).first()
        if(order == None):
            order = Order(event=event, client=event.client, primary_warehouse=warehouse)
            order.save()
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        selected_items = order.items.all()

        products = Product.objects.all()
        added_ids = [selected_item.w_product.product.id for selected_item in selected_items]
        products = products.exclude(id__in=added_ids)
        selected_warehouse_slug = None
        if(warehouse != None):
            if(order):
                order.primary_warehouse = warehouse
                order.save()
            selected_warehouse_slug = warehouse
            selected_warehouse_products = warehouse.products.all()
            inproducts = [product for product in products if getin_warehouse(product, warehouse) != 0]
            outproducts = [product for product in products if getin_warehouse(product, warehouse) == 0]
            context.update({"inproducts": inproducts, "outproducts":outproducts})

            # for other warehouse products
            other_warehouse_products = WarehouseProduct.objects.exclude(warehouses=warehouse)
            products = list(selected_warehouse_products) + list(other_warehouse_products)
        context['product_count'] = selected_items.count()
        context['added_products'] = [item.w_product.id for item in order.items.all()]
        context.update({"allproduct_count":Product.objects.all().count(),"selected_items":selected_items,"warehouses": Warehouse.objects.all(),"order":order, "products": products,"warehouse":warehouse, "selected_warehouse_slug": selected_warehouse_slug, "event":event,})

        return context
    
    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=self.kwargs['event'])
        # order = Order.objects.filter(event=event).first()
        # if(not order):
        order = Order.objects.create(
            client=event.client,
            status="hold",  # Set default status
            order_date=timezone.now()
        )

        # Retrieve submitted product IDs and quantities
        form_data = request.POST.get("jsonData")
        data = json.loads(form_data)
        ids = list(data.keys())
        quantities = list(data.values())
        # Delete existing items in order.items
        # order.items.all().delete()


        for product_id, quantity in zip(ids, quantities):
            # Create OrderItem and associate it with the order
            w_product = WarehouseProduct.objects.get(pk=product_id)
            order_item = OrderItem.objects.create(w_product=w_product, quantity=quantity)
            order.items.add(order_item)

        # Calculate total amount (assuming each product has a price field)
        total_amount = sum(order_item.w_product.product.rental_price * order_item.quantity for order_item in order.items.all())
        order.total_amount = total_amount
        order.event = event
        order.save()
        event.status ="hold"
        event.save()

        return_url = reverse("app-booking-detail", args=[event.id,])
        return redirect(return_url)
    
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





@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@authentication_classes([])
@permission_classes([])
def genquote(request):
    token = request.POST.get('_csrf')
    mid = request.POST.get('id')
    date = timezone.now().date()
    event = get_object_or_404(Event, id=mid)
    event_location = event.location or ""
    formatted_start_date = event.start.strftime("%d/%m/%Y")
    formatted_end_date = event.end.strftime("%d/%m/%Y")
    event_date = f"{formatted_start_date} - {formatted_end_date}"
    contact_person = event.client

    items = [
        {"name": "Guitar", "quantity": 2, "price": "$100"},
        {"name": "Drum Set", "quantity": 1, "price": "$300"},
        {"name": "Microphones", "quantity": 5, "price": "$50"},
    ]

    context = {
        'event_location': event_location,
        'event_date': event_date,
        'contact_person': contact_person,
        'items': items,
        'current_date': timezone.now().date,
        'total': '450.00',
    }

    html_content = render_to_string('pdf_quote.html', context)
    pdf_content = generate_pdf_from_html(html_content)

    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="event_order_quote.pdf"'

    return response

def generate_pdf_from_html(html_content):
    # Function to generate PDF from HTML content
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html_content.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None


def fakegenpdf(request, mid):
    date = timezone.now().date()
    event = get_object_or_404(Event, id=mid)
    event_location = event.location or ""
    formatted_start_date = event.start.strftime("%d/%m/%Y")
    formatted_end_date = event.end.strftime("%d/%m/%Y")
    event_date = f"{formatted_start_date} - {formatted_end_date}"
    contact_person = "Contact Person: John Doe" 

    items = [
        {"name": "Guitar", "quantity": 2, "price": "$100"},
        {"name": "Drum Set", "quantity": 1, "price": "$300"},
        {"name": "Microphones", "quantity": 5, "price": "$50"},
    ]

    context = {
        'event_location': event_location,
        'event_date': event_date,
        'contact_person': contact_person,
        'items': items,
        'current_date': timezone.now().date,
        'total': '450.00',
    }
    return render(request, "pdf_quote.html", context)



class BookingEdit(TemplateView):

    form_class = EventForm

    def get_context_data(self, **kwargs):
        event = get_object_or_404(Event, pk=self.kwargs['id'])
        orders = Order.objects.filter(event=event)
        clients = Client.objects.all()
        warehouses = Warehouse.objects.all()
        t_form = TransferForm()

        # Populate form data based on request method
        form = self.form_class(instance=event)

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = form
        context['t_form'] = t_form
        context['event'] = event
        context['orders'] = orders
        context['clients'] = clients
        context['warehouses'] = warehouses

        return context
    
    def post(self, request, id):
        event = get_object_or_404(Event, pk=id)
        context = self.get_context_data()
        form = EventForm(self.request.POST, instance=event)
        if form.is_valid():
            form.save()  # No need for custom update method
            return redirect(event.get_url())
        else:
            context.update({"message": "Your form contains errors!"})
            return render(request, 'app_booking.html', context)
        
class InvoiceView(TemplateView):

    def get_context_data(self, **kwargs):
        event = get_object_or_404(Event, pk=self.kwargs['id'])
        order = Order.objects.filter(event=event).first()
        try:
            invoice = order.invoice
        except:
            invoice = Invoice(
                order=order
            )
            invoice.save()

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        context['event'] = event
        context['order'] = order
        context['invoice'] = invoice
        return context


    def post(self, request, *args, **kwargs):
        event = self.get_context_data()["event"]
        item_ids = request.POST.getlist('item_ids')
        if item_ids:
            quantities = request.POST.getlist('quantities')
            for item_id, quantity in zip(item_ids, quantities):
                item = get_object_or_404(OrderItem, id=item_id)
                quantity = int(quantity)
                if quantity == 0:
                    item.delete()
                else:
                    item.quantity = quantity
                    item.save()
            return redirect(event.get_url())
        else:
            form = EventForm2(request.POST)
            
            if(form.is_valid()):
                form.update(instance_id=event.id)
                return redirect(event.get_url())
            context = self.get_context_data()
            context.update({"message": "Your form contains errors!", "form": form})
            return render(request, 'app_booking.html', context)


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@authentication_classes([])
@permission_classes([])
def updateorderitemapi(request):
    request_json = json.loads(request.body.decode('utf-8'))
    order_item_id = request_json.get('order_item_id')

    order_item = OrderItem.objects.filter(id=order_item_id).first()
    if(not order_item):
        return JsonResponse({"error":"order item not found"})
    order_item.custom_price = request_json.get('custom_price')
    order_item.quantity = request_json.get('quantity')
    
    order_item.save()
    order_item.order.first().invoice.save()
    return JsonResponse({"message":"Request successfully sent!"})
    



@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@authentication_classes([])
@permission_classes([])
def transfer_request_view(request):
    product_id = request.POST.get('product_id')
    fro = request.POST.get('fro')
    to = request.POST.get('to')
    quantity = request.POST.get('quantity')
    product = Product.objects.filter(id=product_id).first()
    fro = Warehouse.objects.filter(id=fro).first()
    to = Warehouse.objects.filter(id=to).first()
    if(fro == to):
        return JsonResponse({"error":"Can't transfer between the same warehouse!"})
    trans = Transfer(product=product, fro=fro, to=to, count=quantity, trans_type="multiple")
    trans.save()
    return JsonResponse({"message":"request sent successfully!"})


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@authentication_classes([])
@permission_classes([])
def transfer_request_single_view(request):
    barcode = request.POST.get('barcode')
    fro = request.POST.get('fro')
    to = request.POST.get('to')
    if(fro == to):
        return JsonResponse({"error":"Can't transfer between the same warehouse!"})
    item = Item.objects.filter(barcode=barcode).first()
    if(not item):
        return JsonResponse({"error":f'Item with barcode: {barcode} not found!'})
    fro = Warehouse.objects.filter(id=fro).first()
    wp = fro.products.filter(items__in=[item]).first()
    if(not wp):
        return JsonResponse({"error":f'Item with barcode: {barcode} not found in selected warehouse!'})
    to = Warehouse.objects.filter(id=to).first()
    trans = Transfer(item=item, fro=fro, to=to, trans_type="single")
    trans.save()
    return JsonResponse({"message":"request sent successfully!"})