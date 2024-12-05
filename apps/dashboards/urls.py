from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "",
        login_required(DashboardView.as_view(template_name="dashboard.html")),
        name="index",
    ),
    path(
        "dashboard/analytics/",
        login_required(DashboardsView.as_view(template_name="dashboard_analytics.html")),
        name="index2",
    ),

    path(
        "dashboard/crm/",
        login_required(DashboardsView.as_view(template_name="dashboard_crm.html")),
        name="dashboard-crm",
    ),
]
