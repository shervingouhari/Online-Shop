from django.shortcuts import get_object_or_404 as goo404
from django.conf import settings
from shop.serializers import ProductSerializer
from shop.models import Product
from redis import StrictRedis
import json


REDIS = StrictRedis.from_url(settings.REDIS_URL)


class Redis:
    @staticmethod
    def get_prod_key(_id):
        return f"prod-{_id}"

    @staticmethod
    def get_rec_prod_key(_id):
        return f"rec-prod-{_id}"

    @staticmethod
    def add_order(order):
        product_ids = [
            order_product.product.id
            for order_product in order.products.all()
        ]
        for id1 in product_ids:
            for id2 in product_ids:
                if id1 != id2:
                    REDIS.zincrby(Redis.get_rec_prod_key(id1), 1, id2)

    @staticmethod
    def rec_products(products, limit=6):
        if len(products) == 0:
            return None
        product_ids = [product["id"] for product in products]
        keys = [Redis.get_rec_prod_key(_id) for _id in product_ids]
        if len(products) == 1:
            temp = REDIS.zrevrange(keys[0], 0, limit - 1)
        else:
            REDIS.zunionstore("temp", keys)
            REDIS.zrem("temp", *product_ids)
            temp = REDIS.zrevrange("temp", 0, limit - 1)
            REDIS.delete("temp")
        return Product.objects.filter(id__in=[int(i) for i in temp], available=True)

    @staticmethod
    def get_prod_or_404(**kwargs):
        key = Redis.get_prod_key(kwargs["id"])
        value = REDIS.get(key)
        if not value:
            product = goo404(Product, **kwargs)
            serializer = ProductSerializer(nest=True, instance=product)
            value = json.dumps(serializer.data)
            REDIS.setex(key, settings.REDIS_EXPIRATION_TIME, value)
        return json.loads(value)

    @staticmethod
    def update_product(product):
        key = Redis.get_prod_key(product.id)
        value = REDIS.get(key)
        if value:
            if product.available:
                serializer = ProductSerializer(nest=True, instance=product)
                value = json.dumps(serializer.data)
                REDIS.setex(key, settings.REDIS_EXPIRATION_TIME, value)
            else:
                REDIS.delete(key)
