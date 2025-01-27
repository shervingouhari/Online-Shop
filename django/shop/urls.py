from django.urls import path
from .views import product_list, product_detail

app_name = "shop"

urlpatterns = [
    path('', product_list, name="list"),
    path('list/<int:category_id>/<slug:category_slug>/', product_list, name="list"),
    path('detail/<int:product_id>/<slug:product_slug>/', product_detail, name="detail"),
]
