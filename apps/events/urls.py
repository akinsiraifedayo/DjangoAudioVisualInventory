from django.urls import path
from .views import EventFormView, EventView, CompanyView, CompanyFormView, deleteevent, deletecompany
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        "events/edit/<int:id>",
        login_required(EventFormView.as_view(template_name="events_form.html")),
        name="events-edit",
    ),
    path("events/delete/<str:mid>/", deleteevent, name="events-delete"),
    path(
        "events/",
        login_required(EventView.as_view(template_name="events.html")),
        name="events",
    ),
    path(
        "events/<str:event_status>/",
        login_required(EventView.as_view(template_name="events.html")),
        name="eventsfil",
    ),
]