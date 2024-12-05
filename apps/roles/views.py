from django.views.generic import TemplateView
from web_project import TemplateLayout
from .models import Role
from .forms import RoleForm
from django.contrib import messages
from apps.users.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to form_layouts/urls.py file for more pages.
"""


class RolesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        form = RoleForm()
        users= User.objects.all()
        musers = {
        "data":[]
        }
        eusers =[]
        for user in users:
            nuser = {
                "id": user.id,
                "full_name": user.get_name() or "N/A",
                "role": user.get_roles(),
                "username": user.username,
                "email": user.email,
                "status": user.get_fake_status(),
                "avatar": user.Profile_pic.url if user.Profile_pic else "",
            }
            eusers.append(nuser)
        musers["data"] = eusers
        context['ausers'] = musers
        context.update({"roles":Role.objects.all(), "form":form})
        return context

    def post(self, request):
        form = RoleForm(self.request.POST)
        context = self.get_context_data()
        if(form.is_valid()):
            instance = form.save()
            messages.success(request, 'Role Created Successfully!')
            return render(request, 'app_role_list.html', context)
        else:
            context = self.get_context_data()
            context.update({"message": "Your form contains errors!", "form":form})
            return render(request, 'app_role_list.html', context)



class RoleDetailView(TemplateView):
    template_name = 'app_role_detail.html'  # Specify your template name here

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        role = get_object_or_404(Role, id=self.kwargs.get('id'))
        users = role.user_set.all()  # Assuming you have a ManyToManyField from User to Role
        allusers = User.objects.exclude(roles=role)
        form = RoleForm(instance=role)
        musers = {
        "data":[]
        }
        eusers =[]
        for user in users:
            nuser = {
                "id": user.id,
                "full_name": user.get_name() or "N/A",
                "role": user.get_roles(),
                "username": user.username,
                "email": user.email,
                "status": user.get_fake_status(),
                "avatar": user.Profile_pic.url if user.Profile_pic else "",
            }
            eusers.append(nuser)
        musers["data"] = eusers
        context['ausers'] = musers
        context.update({"role": role, "form": form, "users": users, "allusers":allusers})
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = RoleForm(request.POST)
        if form.is_valid():
            role = get_object_or_404(Role, id=self.kwargs.get('id'))
            form.update(instance_id=role.id)
            messages.success(request, 'Role Updated Successfully!')
            return render(request, 'app_role_detail.html', self.get_context_data())
        else:
            context = self.get_context_data()
            context.update({"message": "Your form contains errors!", "form": form})
            return render(request, 'app_role_detail.html', context)







@csrf_exempt
def handlerole(request):
    if request.method == 'POST':
        # Extract form data from the request
        role = request.POST.get('role')
        users = request.POST.get('users')
        # Check if role and users are present
        if role is None or users is None:
            return JsonResponse({'error': 'Role and/or users fields are missing'}, status=400)
        role = get_object_or_404(Role, id=role)
        users = users.split(" ")
        for use in users:
            try:
                int(use)
                user = User.objects.filter(id=use).first()
                if(user != None):
                    user.roles.add(role)
                    user.save()
            except ValueError:
                pass
            except TypeError:
                pass
        # Return a JSON response indicating success
        messages.success(request, 'Role Assigned Successfully!')
        return JsonResponse({'message': 'Form data received successfully'})
    else:
        # Return a JSON response with an error message if the request method is not POST
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def unassignRole(request, id, uid):
    role = get_object_or_404(Role, id=id)
    user = get_object_or_404(User, id=uid)
    user.roles.remove(role)
    user.save()
    return redirect('app-role-detail', role.id)