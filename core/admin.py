from django.contrib import admin
from .models import Customer, Product, OrderProduct, Order

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
