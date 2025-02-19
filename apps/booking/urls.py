from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        "booking/",
        login_required(BookingView.as_view(template_name="app_booking.html")),
        name="app-booking",
    ),
    path(
        "event/<str:id>/",
        login_required(BookingDetails.as_view(template_name="app_booking_detail.html")),
        name="app-booking-detail",
    ),
    path(
        "event/<str:id>/edit/",
        login_required(BookingEdit.as_view(template_name="app_booking_edit.html")),
        name="app-booking-edit",
    ),
    path(
        "scan/<str:id>/",
        login_required(BookingScan.as_view(template_name="scan_page.html")),
        name="scan",
    ),
    path(
        'events/<int:event_id>/delete/', 
        login_required(BookingView.as_view(template_name="app_booking.html")),
        name='delete_event'),
    path(
        "app/event/product/<str:event>/",
        login_required(EventProductView.as_view(template_name="event_product.html")),
        name="event-product-list",
    ),
    path(
        "app/event/product/<str:event>/<str:warehouse>/",
        login_required(EventProductWareView.as_view(template_name="event_product.html")),
        name="eventproductsfil",
    ),
    path("event/<str:id>/remove/client/",
        login_required(BookingDetailsRemove),
        name="app-booking-detail-remove",
    ),
    path(
        "event/clients/add/<str:id>/",
        login_required(ClientFormView.as_view(template_name="add_clients.html")),
        name="event-clients-add",
    ),
    path(
        "event/generate/quote",
        genquote,
        name="event-gen-quote",
    ),
    path(
        "event/generate/quote/<str:mid>/",
        fakegenpdf,
        name="event-gen-quote2",
    ),
    path(
        "event/scan/item/api/",
        scanitemapi,
        name="scan-item-api",
    ),
    path(
        "event/transfer/item/api/",
        transitemapi,
        name="trans-item-api",
    ),
    path(
        "event/remove/item/<str:id>/<str:order_id>/",
        removeorderitem,
        name="remove-item",
    ),
    path(
        "event/add/item/to/quote/",
        additemtoquote,
        name="add-item-to-quote",
    ),
    path(
        "event/remove/item/in/quote/<str:item_id>/<str:order_id>/",
        removequoteitem,
        name="remove-quote-item",
    ),
    path(
        "event/change/to/hold/<str:order_id>/",
        changetohold,
        name="change-to-hold",
    ),
    path(
    "invoice/edit/<str:id>/",
    login_required(InvoiceView.as_view(template_name="edit_invoice.html")),
    name="invoice-edit",
    ),
    path(
    "invoice/preview/<str:id>/",
    login_required(InvoiceView.as_view(template_name="preview_invoice.html")),
    name="invoice-preview",
    ),
    path(
    "invoice/print/<str:id>/",
    login_required(InvoiceView.as_view(template_name="print_invoice.html")),
    name="invoice-print",
    ),
    path(
        "orderitem/update/",
        updateorderitemapi,
        name="update-order-item-api",
    ),
    path(
        "transfer/request/multiple/",
        transfer_request_view,
        name="transfer-request-multiple"
    ),
    path(
        "transfer/request/single/",
        transfer_request_single_view,
        name="transfer-request-single"
    ),

]
fakegenpdf