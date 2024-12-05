from django import forms

from apps.booking.models import Client, Company

class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in ["title","first_name","middle_name","last_name","email","mobile", "phone", "street", "houseNo", "postal", "state", "country"]:
            self.fields[i].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'Write title here'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Write first name here'
        self.fields['middle_name'].widget.attrs['placeholder'] = 'Write middle name here'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Write last name here'
        self.fields['email'].widget.attrs['placeholder'] = 'Write email here'
        self.fields['mobile'].widget.attrs['placeholder'] = 'Write mobile phone here'
        self.fields['phone'].widget.attrs['placeholder'] = 'Write phone number here'
        self.fields['street'].widget.attrs['placeholder'] = 'Write street here'
        self.fields['houseNo'].widget.attrs['placeholder'] = 'Write house number here'
        self.fields['postal'].widget.attrs['placeholder'] = 'Write postal code here'
        self.fields['state'].widget.attrs['placeholder'] = 'Write state here'
        self.fields['country'].widget.attrs['placeholder'] = 'Write country here'
        self.fields['company'].widget.attrs['class'] = 'form-select'

    class Meta:
        model = Client
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
