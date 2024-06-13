from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from core.redis import Redis
from shop.models import Product
from coupon.forms import CouponApplyForm
from .forms import CartAddForm
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = CartAddForm(max_value=product.quantity, data=request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        Cart(request).add_product(product, quantity)
    return redirect('cart:detail')


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart(request).remove_product(product)
    return redirect('cart:detail')


def cart_detail(request):
    cart = Cart(request, validate=True)
    form = CouponApplyForm()
    rec_products = Redis.rec_products([product for product in cart])
    if request.method == 'POST':
        if 'coupon_code' in request.POST:
            form = CouponApplyForm(request.POST)
            if form.is_valid() and form.clean_total_price(cart.total_price()):
                coupon = form.cleaned_data['coupon_code']
                cart.add_coupon(coupon)
        else:
            cart.remove_coupon()
    return render(request, 'cart_detail.html', {
        'form': form,
        'rec_products': rec_products
    })
