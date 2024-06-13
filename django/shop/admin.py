from django.contrib import admin
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from parler.admin import TranslatableAdmin
from .models import Category, Product, Image


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    @admin.display(description=_('decrypted session data'))
    def decrypted_session_data(self, obj):
        return obj.get_decoded()

    list_display = ['session_key', 'expire_date']
    readonly_fields = ['decrypted_session_data'] if settings.DEBUG else []


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['id', 'name', 'slug']
    fields = ['id', 'name', 'slug']
    readonly_fields = ['id', 'slug']


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    class InlineImageAdmin(admin.TabularInline):
        model = Image
        extra = 0
        
    inlines = [InlineImageAdmin]
    list_display = ['id', 'category', 'name', 'slug', 'price', 'quantity', 'available', 'created', 'updated']
    list_filter = ['available']
    list_editable = ['quantity', 'available']
    fields = ['id', 'category', 'name', 'slug', 'description', 'price', 'quantity', 'available', 'created', 'updated']
    readonly_fields = ['id', 'slug', 'created', 'updated']
