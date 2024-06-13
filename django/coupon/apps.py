from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CouponConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coupon'
    verbose_name = _('Coupon')
