from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Coupon


class CouponApplyForm(forms.Form):
    def clean_coupon_code(self):
        now = timezone.now()
        code = self.cleaned_data['coupon_code']
        try:
            return Coupon.objects.get(
                code=code,
                is_valid_from__lte=now,
                is_valid_until__gte=now,
                active=True,
            )
        except Coupon.DoesNotExist:
            raise forms.ValidationError(
                _('Invalid coupon code')
            )

    def clean_total_price(self, total_price):
        if self.cleaned_data['coupon_code'].discount >= total_price:
            self.add_error(
                'coupon_code',
                _('Discount exceeds total price')
            )
            return False
        else:
            return True

    coupon_code = forms.CharField(label='', widget=forms.widgets.TextInput(
        attrs={'placeholder': _('Coupon Code')}
    ))
