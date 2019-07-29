from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

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


def add_product_to_order(request, slug):
    product = get_object_or_404(Product, slug=slug)


@login_required
def customers(request):
    context = {
        'customers': Customer.objects.all()
    }
    return render(request, 'core/customers.html', context)


# @login_required
# def orders(request):
#     context = {
#         'orders': Order.objects.all()
#     }
#     return render(request, 'core/orders.html', context)


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
