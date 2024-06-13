from django.shortcuts import render, redirect
from django.urls import reverse
from cart.cart import Cart
from .forms import OrderCreationForm
from .tasks import check_payment_completion


def order_create(request):
    form = OrderCreationForm()
    cart = Cart(request, validate=True)
    if request.method == "POST":
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.discount = cart.coupon["discount"] if cart.coupon else 0
            order.save()
            order.add_products(cart)
            check_payment_completion.apply_async(args=[order.id], countdown=12 * 60)
            return redirect(reverse("zarinpal:request", args=[order.id]))
    return render(request, "order_create.html", {"form": form})
