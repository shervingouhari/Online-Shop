from django.db import models
from django.utils.translation import gettext_lazy as _
import secrets


class Coupon(models.Model):
    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = secrets.token_urlsafe(10)
        super().save(*args, **kwargs) 
    
    def decrease_max_usage(self):
        self.max_usage -= 1
        if self.max_usage == 0:
            self.active = False
        self.save()

    code = models.CharField(_('code'), max_length=20, unique=True, blank=True, db_index=True)
    is_valid_from = models.DateTimeField(_('is valid from'))
    is_valid_until = models.DateTimeField(_('is valid until'))
    discount = models.PositiveIntegerField(_('discount'))
    max_usage = models.PositiveIntegerField(_('max usage'))
    active = models.BooleanField(_('active'))
