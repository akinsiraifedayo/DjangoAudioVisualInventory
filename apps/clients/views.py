from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.booking.models import Client, Company
from .forms import ClientForm, CompanyForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to clients/urls.py file for more pages.
"""

class ClientView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        company_id = self.kwargs.get('company_id') 
        clients = Client.objects.all()  # Default to all clients
        selected_company_id = company_id if company_id and company_id != "ALL" else None

        if company_id is not None and company_id != "ALL":
            clients = Client.objects.filter(company_id=company_id)
        company_count = clients.count()
        context['client_count'] = company_count
        context['clients'] = clients
        context['companies'] = Company.objects.all()
        context['selected_company_id'] = selected_company_id
        return context


class ClientFormView(TemplateView):
    # template_name = 'add_clients.html'
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        client_id = self.kwargs.get('id')
        context['form'] = self.form_class()
        if client_id:
            client = get_object_or_404(Client, pk=client_id)
            context['client'] = client
            context['form'] = self.form_class(instance=client)
        context['companies'] = Company.objects.all()  # Add this line to fetch companies
        return context

    def post(self, request, *args, **kwargs):
        client_id = self.kwargs.get('id')
        if client_id:
            client = get_object_or_404(Client, pk=client_id)
            form = self.form_class(request.POST, instance=client)
        else:
            form = self.form_class(request.POST)
        print("form is", form)
        if form.is_valid():
            form.save()
            return redirect('clients')  # Redirect to the success URL
        else:
            return render(request, self.template_name, {'form': form})
        


class CompanyView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        companies = Company.objects.all()
        company_count = companies.count()
        print("company count is", company_count)
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
        print("form is", form)
        if form.is_valid():
            form.save()
            return redirect('companies')  # Redirect to the success URL
        else:
            return render(request, self.template_name, {'form': form})


def deleteclient(request,mid):
    client = Client.objects.filter(id=mid).first()
    client.delete()
    return redirect('clients')

def deletecompany(request,mid):
    company = Company.objects.filter(id=mid).first()
    company.delete()
    return redirect('companies')
