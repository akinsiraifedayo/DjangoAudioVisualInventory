from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','username', 'password', 'email', 'first_name', 'last_name', 'is_salesperson', 'is_operations_manager', 'is_equipment_manager', 'is_warehouse_staff', 'is_technician', 'is_account_manager', 'is_account_department', 'Gender', 'Phone_number', 'Profile_pic']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Customize form fields as per your requirements, add additional attributes if necessary

    def clean_Profile_pic(self):
        # This method ensures that the profile pic URL is provided if no new image is uploaded during update
        cleaned_data = super().clean()
        profile_pic = cleaned_data.get("Profile_pic")
        if not profile_pic:
            profile_pic = self.instance.Profile_pic  # Get the existing profile pic URL
        return profile_pic
