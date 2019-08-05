from rest_framework import serializers

from core.models import Customer, Order, OrderProduct, Product


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'city', 'phone_number', 'street', 'zip']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()

    def get_customer_name(self, obj):
        return Customer.objects.get(id=obj.customer_id).name

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'user_id', 'created_at', 'customer_name']


class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return Product.objects.get(id=obj.product_id).title

    class Meta:
        model = OrderProduct
        fields = ['id', 'order_id', 'product_id', 'quantity', 'created_at', 'updated_at', 'product_name']
