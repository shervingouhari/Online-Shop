from rest_framework import serializers
from shop.models import Category, Product, Image


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'names', 'slug', 'get_absolute_url', 'products']

    def __init__(self, nest=False, *args, **kwargs):
        self.nest = nest
        super().__init__(*args, **kwargs)

    def get_names(self, obj):
        return {
            i["language_code"]: i['name']
            for i in obj.translations.values()
        }

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    def get_products(self, obj):
        if self.nest:
            return ProductSerializer(instance=obj.products, many=True).data
        return [product.id for product in obj.products.all()]

    names = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'names',
            'slug',
            'descriptions',
            'price',
            'quantity',
            'available',
            'created',
            'updated',
            'get_absolute_url',
            'get_first_image',
            'images',
        ]

    def __init__(self, nest=False, *args, **kwargs):
        self.nest = nest
        super().__init__(*args, **kwargs)

    def get_category(self, obj):
        if self.nest:
            return CategorySerializer(instance=obj.category).data
        return obj.category.id

    def get_names(self, obj):
        return {
            i["language_code"]: i['name']
            for i in obj.translations.values()
        }

    def get_descriptions(self, obj):
        return {
            i["language_code"]: i['description']
            for i in obj.translations.values()
        }

    def get_images(self, obj):
        if self.nest:
            return ImageSerializer(instance=obj.images, many=True).data
        return [image.id for image in obj.images.all()]

    category = serializers.SerializerMethodField()
    names = serializers.SerializerMethodField()
    descriptions = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'product', 'image', 'get_url']

    def __init__(self, nest=False, *args, **kwargs):
        self.nest = nest
        super().__init__(*args, **kwargs)

    def get_url(self, obj):
        return obj.get_url()

    def get_product(self, obj):
        if self.nest:
            return ProductSerializer(instance=obj.product).data
        return obj.product.id

    product = serializers.SerializerMethodField()
