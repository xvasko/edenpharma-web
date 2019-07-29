from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.models import Product, Customer, Order, OrderProduct


@login_required
def index(request):
    return render(request, 'core/index.html')


# @login_required
# def products(request):
#     context = {
#         'products': Product.objects.all()
#     }
#     return render(request, 'core/products.html', context)


class ProductView(ListView):
    model = Product
    template_name = 'core/products.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'core/product.html'


class ProductCreate(CreateView):
    model = Product
    fields = ['title']
    success_url = reverse_lazy('core:products')


class ProductUpdate(UpdateView):
    model = Product
    fields = ['title']
    success_url = reverse_lazy('core:products')


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('core:products')


# @login_required
# def customers(request):
#     context = {
#         'customers': Customer.objects.all()
#     }
#     return render(request, 'core/customers.html', context)


class CustomerView(ListView):
    model = Customer
    template_name = 'core/customers.html'


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'core/customer.html'


class CustomerCreate(CreateView):
    model = Customer
    fields = ['name']
    success_url = reverse_lazy('core:customers')


class CustomerUpdate(UpdateView):
    model = Customer
    fields = ['name']
    success_url = reverse_lazy('core:customers')


class CustomerDelete(DeleteView):
    model = Customer
    success_url = reverse_lazy('core:customers')








class OrderView(ListView):
    model = Order
    template_name = 'core/orders.html'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'core/order.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['order_product_list'] = OrderProduct.objects.filter(order_id=self.get_object().id)
        return context
