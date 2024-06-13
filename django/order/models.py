from django.db import models
from django.utils.translation import gettext_lazy as _
from shop.models import Product
from core.redis import Redis


class Order(models.Model):
    class Meta:
        ordering = ['-created']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return str(self.id)

    def add_products(self, cart):
        for product in cart:
            OrderProduct.objects.create(
                order=self,
                product=Product.objects.get(id=product['id']),
                quantity=product['requested_quantity'],
            )
        Redis.add_order(self)
        self.update_products(action='decrease stock')

    def update_products(self, action):
        for order_product in self.products.all():
            product = order_product.product
            if action == 'decrease stock':
                product.quantity -= order_product.quantity
                product.available = False if product.quantity == 0 else True
            elif action == 'increase stock':
                product.quantity += order_product.quantity
                product.available = True
            product.save()

    def get_total_price(self):
        result = sum(product.get_price() for product in self.products.all())
        return result - self.discount

    STATUS_CHOICES = [
        ('1', _('awaiting payment')),
        ('2', _('awaiting shipment')),
        ('3', _('awaiting delivery')),
        ('4', _('delivered')),
    ]
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    email = models.EmailField(_('email'))
    city = models.CharField(_('city'), max_length=100)
    address = models.TextField(_('address'))
    postal_code = models.PositiveIntegerField(_('postal code'))
    discount = models.PositiveIntegerField(_('discount'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('update'), auto_now=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='1')


class OrderProduct(models.Model):
    class Meta:
        verbose_name = _('Order Product')
        verbose_name_plural = _('Order Products')

    def __str__(self):
        return str(self.id)

    def get_price(self):
        return self.product.price * self.quantity

    order = models.ForeignKey(Order, verbose_name=_('order'), related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('quantity'))
