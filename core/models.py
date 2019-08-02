from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    street = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    zip = models.CharField(max_length=128, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(editable=False, null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Customer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:customer', kwargs={'pk': self.id})


class Product(models.Model):
    title = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(editable=False, null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:product', kwargs={'pk': self.id})


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False, null=True)

    def save(self, *args, **kwargs):
        # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078
        if not self.id:
            self.created_at = timezone.now()
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f'Objednavka #{self.id} pre {self.customer.name}'


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(editable=False, null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(OrderProduct, self).save(*args, **kwargs)
