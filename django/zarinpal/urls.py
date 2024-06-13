from django.urls import path
from .views import send_request, verify

app_name = 'zarinpal'

urlpatterns = [
    path('request/<int:order_id>/', send_request, name='request'),
    path('verify/<int:order_id>/', verify, name='verify'),
]
