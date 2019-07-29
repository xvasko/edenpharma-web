from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(default='default')

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    slug = models.SlugField(default='default')

    def __str__(self):
        return f'Objednavka #{self.id} pre {self.customer.name}'


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.title
