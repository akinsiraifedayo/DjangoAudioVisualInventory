from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.booking.models import *
from .forms import EventForm, CompanyForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to events/urls.py file for more pages.
"""

class EventView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        event_status = self.kwargs.get('event_status') 
        events = Event.objects.all()  # Default to all events
        
        event_status_choices = order_statuses
        selected_event_status = event_status if event_status and event_status != "ALL" else None

        if event_status is not None and event_status != "ALL":
            events = Event.objects.filter(status=event_status)
        event_count = events.count()
        context['event_count'] = event_count
        context['events'] = events
        context['event_status_choices'] = event_status_choices
        context['companies'] = Company.objects.all()
        context['selected_event_status'] = selected_event_status
        return context

class EventFormView(TemplateView):
    template_name = 'events_form.html'
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        client_id = self.kwargs.get('id')
        context['form'] = self.form_class()
        if client_id:
            client = get_object_or_404(Event, pk=client_id)
            context['client'] = client
            context['form'] = self.form_class(instance=client)
        context['companies'] = Company.objects.all()  # Add this line to fetch companies
        return context

    def post(self, request, *args, **kwargs):
        client_id = self.kwargs.get('id')
        if client_id:
            client = get_object_or_404(Event, pk=client_id)
            form = self.form_class(request.POST, instance=client)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events')  # Redirect to the success URL
        else:
            return render(request, self.template_name, {'form': form})
        


class CompanyView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        companies = Company.objects.all()
        company_count = companies.count()
        context.update({"companies": Company.objects.all(), "company_count": company_count})

        return context
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CompanyFormView(TemplateView):
    template_name = 'add_companies.html'
    form_class = CompanyForm

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        company_id = self.kwargs.get('id')
        if company_id:
            company = get_object_or_404(Company, pk=company_id)
            context['company'] = company
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        company_id = self.kwargs.get('id')
        if company_id:
            company = get_object_or_404(Company, pk=company_id)
            form = self.form_class(request.POST, instance=company)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('companies')  # Redirect to the success URL
        else:
            return render(request, self.template_name, {'form': form})


def deleteevent(request,mid):
    client = Event.objects.filter(id=mid).first()
    client.delete()
    return redirect('events')

def deletecompany(request,mid):
    company = Company.objects.filter(id=mid).first()
    company.delete()
    return redirect('companies')


