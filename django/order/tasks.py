from celery import shared_task


@shared_task
def check_payment_completion(order_id):
    from order.models import Order
    order = Order.objects.get(id=order_id)
    if order.status == '1':
        order.update_products(action='increase stock')
