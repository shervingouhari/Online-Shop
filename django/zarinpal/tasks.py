from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import activate, gettext_lazy as _
from django.conf import settings
from core.builtins import number_translator
from celery import shared_task
from weasyprint import HTML
from order.models import Order


@shared_task
def send_success_email(order_id, language):
    activate(language)
    order = get_object_or_404(Order, id=order_id)
    subject = f'{_("Invoice Number")} {number_translator(order.id)}'
    message = f'{order.first_name} {order.last_name}\n{_("Your order was placed successfully")}'
    from_email = settings.EMAIL_HOST_USER
    html = render_to_string('order_pdf.html', {"orders": [order]})
    pdf_data = HTML(string=html).write_pdf()
    email = EmailMessage(subject, message, from_email, [order.email])
    email.attach("Receipt.pdf", pdf_data, "application/pdf")
    email.send()
