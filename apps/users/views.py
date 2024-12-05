from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import User
from .forms import UserForm
from web_project import TemplateLayout  
from django.shortcuts import render, redirect, get_object_or_404
import random
from apps.roles.models import Role
# Import your TemplateLayout

class UsersView(PermissionRequiredMixin, TemplateView):
    permission_required = ("user.view_user", "user.delete_user", "user.change_user", "user.add_user")
    template_name = 'app_user_list.html'
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        wusers = User.objects.all()
        musers = {
        "data":[]
        }
        eusers =[]
        for user in wusers:
            nuser = {
                "id": user.id,
                "full_name": user.get_name() or "N/A",
                "role": "Author",
                "username": user.username,
                "email": user.email,
                "current_plan": "Team",
                "billing": "Manual - Paypal",
                "status": user.get_fake_status(),
                "avatar": user.Profile_pic.url if user.Profile_pic else "",
            }
            eusers.append(nuser)
        musers["data"] = eusers
        context['ausers'] = musers
        context['user'] = None
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create a User instance but don't save it to the database yet
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            context = self.get_context_data()
            return render(request, self.template_name, context)
        else:
            context = self.get_context_data()
            context.update({"message": "Your form contains errors!", "form":form})
            return render(request, self.template_name, context)
        

    def delete(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return render(request, self.template_name, self.get_context_data())  # Redirect to user list page

    def update(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, self.get_context_data())  # Redirect to user list page
        else:
            return render(request, self.template_name, {'form': form})



class UsersDetailView(PermissionRequiredMixin, TemplateView):
    permission_required = ("user.view_user")
    template_name = 'app_user_view_account2.html'
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_id = self.kwargs.get('id')
        user = get_object_or_404(User, id=user_id)

        permissions =[]
        field_descriptions = Role.get_field_descriptions()
        for role in user.roles.all():
            true_fields = [field for field, value in role.__dict__.items() if value and field in field_descriptions]
            
            # Print descriptions of True fields for this role
            for field in true_fields:
                permissions.append(f"{field_descriptions[field]}")
        permissions =set(permissions)
        context["user"] = user
        context["permissions"] = permissions
        return context

class UsersRoleView(PermissionRequiredMixin, TemplateView):
    permission_required = ("user.view_user")
    template_name = 'app_user_view_account2.html'
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_id = self.kwargs.get('id')
        user = get_object_or_404(User, id=user_id) 
        context["user"] = user
        return context