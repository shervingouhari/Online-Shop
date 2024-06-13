from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from coupon.models import Coupon
from order.models import Order
from cart.cart import Cart
from .tasks import send_success_email
import requests
import json


ZARINPAL_MERCHANT_ID = settings.ZARINPAL_MERCHANT_ID
ZARINPAL_SUBDOMAIN = 'sandbox' if ZARINPAL_MERCHANT_ID == '00000000-0000-0000-0000-000000000000' else 'www'
ZARINPAL_API_REQUEST = f"https://{ZARINPAL_SUBDOMAIN}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZARINPAL_API_VERIFY = f"https://{ZARINPAL_SUBDOMAIN}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZARINPAL_API_STARTPAY = f"https://{ZARINPAL_SUBDOMAIN}.zarinpal.com/pg/StartPay/"


def send_request(request, order_id):
    order = Order.objects.get(id=order_id)
    callbackURL = request.build_absolute_uri(
        reverse("zarinpal:verify", args=[order.id])
    )
    data = {
        "MerchantID": ZARINPAL_MERCHANT_ID,
        "Amount": order.get_total_price(),
        "Currency": "IRT",
        "Description": "description",
        "Email": order.email,
        "CallbackURL": callbackURL,
    }
    headers = {
        "content-type": "application/json",
        "content-length": str(len(data))
    }
    data = json.dumps(data)

    try:
        response = requests.post(
            ZARINPAL_API_REQUEST, data=data, headers=headers, timeout=10
        )
        response = response.json()
        if response["Status"] == 100:
            return redirect(ZARINPAL_API_STARTPAY + str(response["Authority"]))
        error = f"{response['Status']} status code"
    except requests.exceptions.Timeout:
        error = "timeout error"
    except requests.exceptions.ConnectionError:
        error = "connection error"
    return render(request, "zarinpal_failure.html", {"error": error if "error" in locals() else None})


def verify(request, order_id):
    cart = Cart(request)
    order = Order.objects.get(id=order_id)
    data = {
        "MerchantID": ZARINPAL_MERCHANT_ID,
        "Amount": order.get_total_price(),
        "Currency": "IRT",
        "Authority": request.GET["Authority"],
    }
    data = json.dumps(data)
    headers = {
        "content-type": "application/json",
        "content-length": str(len(data))
    }

    try:
        response = requests.post(
            ZARINPAL_API_VERIFY, data=data, headers=headers, timeout=10
        )
        response = response.json()
        if response["Status"] == 100 or response["Status"] == 101:
            order.status = "2"
            order.save()
            if cart.coupon:
                coupon = Coupon.objects.get(id=cart.coupon["id"])
                coupon.decrease_max_usage()
            cart.delete()
            send_success_email.delay(order.id, request.LANGUAGE_CODE)
            return render(request, "zarinpal_success.html", {"RefID": response["RefID"]})
        error = f"{response['Status']} status code"
    except requests.exceptions.Timeout:
        error = "timeout error"
    except requests.exceptions.ConnectionError:
        error = "connection error"
    return render(request, "zarinpal_failure.html", {"error": error if "error" in locals() else None})
