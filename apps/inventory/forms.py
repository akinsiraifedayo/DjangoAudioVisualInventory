from django import forms

from .models import Product, Category
from django.db.utils import OperationalError

class ProductForm(forms.ModelForm):
    choices = [
        ("guitars", "Guitars"),
        ("bass_guitars", "Bass Guitars"),
        ("keyboards", "Keyboards"),
        ("synthesizers", "Synthesizers"),
        ("drum_kits", "Drum Kits"),
        ("percussion_instruments", "Percussion Instruments"),
        ("microphones", "Microphones"),
        ("amplifiers", "Amplifiers"),
        ("audio_interfaces", "Audio Interfaces"),
        ("studio_monitors", "Studio Monitors"),
        ("headphones", "Headphones"),
        ("dj_equipment", "DJ Equipment"),
        ("electronic_drums", "Electronic Drums"),
        ("midi_controllers", "MIDI Controllers"),
        ("effects_pedals", "Effects Pedals"),
        ("wind_instruments", "Wind Instruments"),
        ("string_instruments", "String Instruments"),
        ("audio_mixers", "Audio Mixers"),
        ("recording_accessories", "Recording Accessories"),
        ("cables_and_connectors", "Cables and Connectors"),
    ]
    # Dynamically fetch choices from the Category model
    try:
        cchoices = Category.objects.values_list('slug', 'name')
        # Combine predetermined choices with dynamic choices
        choices = choices + list(cchoices)
    except OperationalError:
        pass

    category = forms.ChoiceField(
        choices=choices,
        label='Select a category',
        widget=forms.Select(attrs={'class': 'select2 form-select form-control'})  # Optional: Add Bootstrap class for styling
    )

    #purchase_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "html5-date-input", 'type':'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in ["image","name","manufacturer", "rental_price", "item_type"]:
            self.fields[i].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Write product name here'
        self.fields['manufacturer'].widget.attrs['placeholder'] = 'Product Manufacturer'
        self.fields['availability'].widget.attrs['class']="form-check-input"
        self.fields['image'].widget.attrs['id']= "formFile"
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        if not image and self.instance:
            cleaned_data['image'] = self.instance.image
        return cleaned_data