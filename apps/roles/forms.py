from django import forms
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Role

class RoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize field IDs
        for field_name in self.fields:
            if field_name not in ['name', 'description']:
                self.fields[field_name].widget.attrs['id'] = field_name + 'Read'
                self.fields[field_name].widget.attrs['class'] = 'form-check-input'
            else:
                if(field_name == 'name'):
                    self.fields[field_name].widget.attrs['placeholder'] = 'Enter a Role Name'
                    self.fields[field_name].required = True
                else:
                    self.fields[field_name].widget.attrs['placeholder'] = 'Enter a Description for the Role'
                self.fields[field_name].widget.attrs['class'] = 'form-control'

    def update(self, instance_id=None):
        if instance_id:
            instance = get_object_or_404(Role, pk=instance_id)
            for field in self.fields:
                setattr(instance, field, self.cleaned_data[field])
            instance.save()
        else:
            raise Http404("Role Not Found")


    class Meta:
        model = Role
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 3, 'rows': 5}),  # Customize the Textarea widget for description field
        }
