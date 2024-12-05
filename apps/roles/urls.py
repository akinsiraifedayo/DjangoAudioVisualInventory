from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "app/roles/manage/",
        login_required(RolesView.as_view(template_name="app_role_list.html")),
        name="app-role-list",
    ),
    path(
        "app/roles/manage/<str:id>/",
        login_required(RoleDetailView.as_view(template_name="app_role_detail.html")),
        name="app-role-detail",
    ),
    path(
        "app/roles/manage/<str:id>/<str:uid>/unassign/",
        login_required(unassignRole),
        name="app-role-detail-unassign",
    ),
    path(
        "app/roles/assign/users/",
        login_required(handlerole),
        name="app-role-assign-users",
    ),
]