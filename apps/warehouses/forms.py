from django import forms
from .models import Warehouse, WarehouseProduct, Transfer

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'

class WarehouseProductForm(forms.ModelForm):
    class Meta:
        model = WarehouseProduct
        fields = '__all__'

class TransferForm(forms.ModelForm):
    item_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Transfer
        fields = ['fro', 'to', 'count']