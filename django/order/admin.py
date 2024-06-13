from django.template.loader import render_to_string
from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from core.builtins import intcomma
from .models import Order, OrderProduct
from datetime import datetime
from weasyprint import HTML
import csv


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    class InlineOrderProductAdmin(admin.TabularInline):
        @admin.display(description=_('unit price'))
        def unit_price(self, obj):
            return intcomma(obj.product.price)

        @admin.display(description=_('total price'))
        def total_price(self, obj):
            return intcomma(obj.get_price())

        model = OrderProduct
        extra = 0
        readonly_fields = ['unit_price', 'total_price']

    @admin.display(description=_('total price'))
    def total_price(self, obj):
        return intcomma(obj.get_total_price())

    @admin.action(description=_("Export to CSV"))
    def export_csv(self, request, queryset):
        content = 'attachment; filename=Receipt.csv'
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response['Content-Disposition'] = content
        response.write(u'\ufeff'.encode('utf8'))
        csv_data = csv.writer(response)

        fields = [
            field for field in self.model._meta.get_fields()
            if not field.many_to_many and not field.one_to_many
        ]

        csv_data.writerow([field.verbose_name for field in fields])
        for obj in queryset:
            row = []
            for field in fields:
                value = getattr(obj, field.name)
                if field.name == "status":
                    value = obj.get_status_display()
                elif isinstance(value, datetime):
                    value = value.strftime('%d/%m/%Y')
                row.append(value)
            csv_data.writerow(row)
        return response

    @admin.action(description=_("Export to PDF"))
    def export_pdf(self, request, queryset):
        html = render_to_string('order_pdf.html', {"orders": queryset})
        pdf_data = HTML(string=html).write_pdf()
        content = 'attachment; filename=Receipt.pdf'
        response = HttpResponse(pdf_data, content_type="application/pdf")
        response['Content-Disposition'] = content
        return response

    inlines = [InlineOrderProductAdmin]
    list_display = [field.name for field in Order._meta.fields]
    list_filter = ['status', 'created', 'updated']
    actions = ["export_csv", "export_pdf"]
    readonly_fields = ['created', 'updated', 'total_price']
