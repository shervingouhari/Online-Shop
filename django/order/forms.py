from django import forms
from .models import Order


class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['created', 'updated', 'status', 'discount']
