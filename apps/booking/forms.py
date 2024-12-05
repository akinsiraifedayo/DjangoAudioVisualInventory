from django import forms
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import *


class EventForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        existing_clients = list(self.fields['client'].choices)
        for i in ["name","start","end","all_day", "location", "description", "client","url","event_manager"]:
            self.fields[i].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Event Name'
        self.fields['project_type'].widget.attrs['class'] ='select2 select-event-label form-select'
        self.fields['event_type'].widget.attrs['class'] ='select2 select-event-label form-select'
        self.fields['event_manager'].widget.attrs['class'] ='select2 select-event-label form-select'
        self.fields['start'].widget.attrs['class']="form-control flatpickr-input flatpickr-mobile"
        self.fields['start'].widget.attrs['id']="eventStartDate"
        self.fields['end'].widget.attrs['id']="eventEndDate"
        self.fields['name'].widget.attrs['id']="eventName"
        self.fields['url'].widget.attrs['id']="eventURL"
        self.fields['location'].widget.attrs['id']="eventLocation"
        self.fields['description'].widget.attrs['id']="eventDescription"
        self.fields['project_type'].widget.attrs['id']="eventLabel"
        self.fields['end'].widget.attrs['class']="form-control flatpickr-input flatpickr-mobile"
        self.fields['all_day'].widget.attrs['class']="switch-input allDay-switch"
        self.fields['url'].widget.attrs['placeholder']='https://www.google.com'
        self.fields['location'].widget.attrs['placeholder']='Enter Location'
        self.fields['client'].widget.attrs['class']= 'select2 form-select form-select-md'
        self.fields['client'].widget.attrs['id']= 'select2Basic2'
        self.fields['client'].widget.attrs['data-allow-clear']= 'true'
        #self.fields['client'].widget.attrs['onchange']= 'refilter(this.value)'


    def update(self, instance):
        instance.name = self.cleaned_data['name']
        instance.project_type = self.cleaned_data['project_type']
        instance.event_type = self.cleaned_data['event_type']
        instance.event_manager = self.cleaned_data['event_manager']
        instance.start = self.cleaned_data['start']
        instance.end = self.cleaned_data['end']
        instance.all_day = self.cleaned_data['all_day']
        instance.location = self.cleaned_data['location']
        instance.description = self.cleaned_data['description']
        instance.client = self.cleaned_data['client']
        instance.url = self.cleaned_data['url']
        instance.save()

    class Meta:
        model = Event
        fields = '__all__'



class EventForm2(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        existing_clients = list(self.fields['client'].choices)
        self.fields['client'].widget.attrs['class']= 'select2 form-select form-select-md'
        self.fields['client'].widget.attrs['id']= 'select2Basic2'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        instance = kwargs.get('instance')
        if instance:
            current_status = instance.status
            if current_status == 'quote':
                self.fields['status'].choices = [('quote','Quote'),('hold', 'Hold')]
            elif current_status == 'hold':
                self.fields['status'].choices = [('hold','Hold'),('ready_to_pack','Ready To Pack'),('packed','Packed')]
            elif(current_status == "ready_to_pack"):
                self.fields['status'].choices = [('ready_to_pack','Ready To Pack'),('packed','Packed')]
            elif (current_status == "packed"):
                self.fields['status'].choices = [('packed','Packed'),('on_site','On Site'),] 
            elif (current_status == "on_site"):
                self.fields['status'].choices = [('on_site','On Site'),('returned','Returned'),]
            elif(current_status == "returned"):
                self.fields['status'].choices = [('returned','Returned'),('invoiced','Invoiced'),]
            elif(current_status == "invoiced"):
                self.fields['status'].choices =[('invoiced','Invoiced'),('paid','Paid'),]




    def update(self, instance_id=None):
        verdict = None
        stats = self.cleaned_data['status']
        if instance_id:
            instance = get_object_or_404(Event, pk=instance_id)
            self.instance = instance
        else:
            raise Http404("Event Not Found")
        order = Order.objects.filter(event=instance).first()
        if(order):
            if(stats == "hold"):
                if(order.items.all().count()):
                    instance.status= stats
                    order.status = stats
                else:
                    verdict = "no quote"
            else:
               instance.status= stats
               order.status = stats 
        else:
            nwOrder = Order(client=instance.client, event=instance)
            nwOrder.save()
            order = nwOrder
            verdict = "no quote"
        client = self.cleaned_data['client']
        if client:
            instance.client = client 
            order.client =client
        instance.save()
        order.save()
        if(verdict):
            return verdict
        return instance
        
    class Meta:
        model = Event
        fields = ('client','status')


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['w_product', 'quantity']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['language', 'due_date', 'total_amount', 'is_paid', 'payment_date']



