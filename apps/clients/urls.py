from django.urls import path
from .views import ClientFormView, ClientView, CompanyView, CompanyFormView, deleteclient, deletecompany
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        "clients/add/",
        login_required(ClientFormView.as_view(template_name="add_clients.html")),
        name="clients-add",
    ),
    path(
        "clients/edit/<int:id>",
        login_required(ClientFormView.as_view(template_name="add_clients.html")),
        name="clients-edit",
    ),
    path("clients/delete/<str:mid>/", deleteclient, name="clients-delete"),
    path(
        "clients/",
        login_required(ClientView.as_view(template_name="clients.html")),
        name="clients",
    ),
    path(
        "clients/<int:company_id>/",
        login_required(ClientView.as_view(template_name="clients.html")),
        name="clientsfil",
    ),
    path(
        "companies/add/",
        login_required(CompanyFormView.as_view(template_name="add_companies.html")),
        name="companies-add",
    ),
    path(
        "companies/update/<int:id>",
        login_required(CompanyFormView.as_view(template_name="add_companies.html")),
        name="companies-update",
    ),
    path("companies/delete/<str:mid>/", 
        deletecompany, 
        name="companies-delete"
    ),
    path(
        "companies/",
        login_required(CompanyView.as_view(template_name="companies.html")),
        name="companies",
    ),
]