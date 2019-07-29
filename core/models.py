from django.db import models
from django.urls import reverse


class Customer(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:customer', kwargs={'pk': self.id})


class Product(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:product', kwargs={'pk': self.id})


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'Objednavka #{self.id} pre {self.customer.name}'


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.title
