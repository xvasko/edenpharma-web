from django.db import models
from django.urls import reverse


class Customer(models.Model):
    name = models.CharField(max_length=128)
    street = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    zip = models.CharField(max_length=128, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:customer', kwargs={'pk': self.id})


class Product(models.Model):
    title = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

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
