from django import forms
from django.utils.translation import gettext_lazy as _


class CartAddForm(forms.Form):
    def __init__(self, max_value, *args, **kwargs):
        self.max_value = max_value
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity > self.max_value:
            raise forms.ValidationError(
                _(f'Quantity exceeds available stock')
            )
        elif quantity < 1:
            raise forms.ValidationError(_('Quantity must greater than zero'))
        return quantity

    quantity = forms.IntegerField()
