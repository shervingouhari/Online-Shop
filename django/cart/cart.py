from shop.models import Product


class Cart:
    def __init__(self, request, validate=False):
        self.session = request.session
        if self.session.get('cart') == None:
            self.session.update({'cart': {}})
        if self.session.get('coupon') == None:
            self.session.update({'coupon': {}})
        self.cart = self.session['cart']
        self.coupon = self.session['coupon']
        if validate:
            self.validate()

    def __len__(self):
        return sum(product['requested_quantity'] for product in self)

    def __iter__(self):
        return iter(self.cart.values())

    def add_product(self, product, quantity):
        product = self.product_to_dict(product, quantity)
        self.cart[str(product['id'])] = product
        self.save()

    def add_coupon(self, coupon):
        self.session['coupon'] = self.coupon_to_dict(coupon)

    def save(self):
        self.session.modified = True

    def remove_product(self, product, remove_all=False):
        if str(product.id) in self.cart:
            if (
                self.cart[str(product.id)]['requested_quantity'] == 1
                or remove_all == True
            ):
                del self.cart[str(product.id)]
            else:
                self.cart[str(product.id)]['requested_quantity'] -= 1
                self.cart[str(product.id)]['total_price'] -= product.price
            self.remove_coupon()
            self.save()

    def remove_coupon(self):
        del self.session['coupon']

    def delete(self):
        del self.session['cart']
        del self.session['coupon']

    def total_price(self):
        return sum(product['total_price'] for product in self.cart.values())

    def product_to_dict(self, product, quantity):
        return {
            'id': product.id,
            'get_absolute_url': product.get_absolute_url(),
            'get_first_image': product.get_first_image(),
            'names': {
                i['language_code']: i['name']
                for i in product.translations.values()
            },
            'requested_quantity': quantity,
            'available_quantity': product.quantity,
            'unit_price': product.price,
            'total_price': quantity * product.price,
        }

    def coupon_to_dict(self, coupon):
        return {
            'id': coupon.id,
            'discount': coupon.discount
        }

    def validate(self):
        products_to_remove = []
        for product in self:
            instance = Product.objects.get(id=product['id'])
            if product['requested_quantity'] > instance.quantity:
                products_to_remove.append(instance)
        for product in products_to_remove:
            self.remove_product(product, remove_all=True)
