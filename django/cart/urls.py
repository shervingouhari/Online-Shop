from django.urls import path
from .views import cart_add, cart_remove, cart_detail

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', cart_add, name='add'),
    path('remove/<int:product_id>/', cart_remove, name='remove'),
    path('detail/', cart_detail, name='detail'),
]
