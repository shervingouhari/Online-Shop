from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Coupon._meta.fields]
    list_filter = ['active', 'is_valid_from', 'is_valid_until']
    list_editable = ['max_usage', 'active']
    fields = [field.name for field in Coupon._meta.fields]
    readonly_fields = ['id']
    search_field = ['code']
