from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.models import Product, Customer, Order, OrderProduct


@login_required
def index(request):
    return render(request, 'core/index.html')


class CustomerRow:
    def __init__(self, customer_name, products):
        self.customer_name = customer_name
        self.products = products


class OverviewView(TemplateView):
    context_object_name = 'context'
    template_name = 'core/overview.html'

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        # context['customers'] = Customer.objects.all()

        num_of_customers = len(Customer.objects.all())
        num_of_products = len(Product.objects.all())
        context['customers'] = [None] * num_of_customers

        for i, customer in enumerate(Customer.objects.all()):
            context['customers'][i] = CustomerRow(customer.name, [0] * num_of_products)
            for j, product in enumerate(Product.objects.all()):
                for order in Order.objects.filter(customer_id=customer.id):
                    for order_product in OrderProduct.objects.filter(order_id=order.id, product_id=product.id):
                        context['customers'][i].products[j] += order_product.quantity

        for customer in context['customers']:
            print(customer)
            print(customer.customer_name)
            print(customer.products)

        return context


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

# ============================
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


# ============================
class OrderView(ListView):
    model = Order
    template_name = 'core/orders.html'


class OrderCreate(CreateView):
    model = Order
    fields = ['customer']

    # success_url = reverse_lazy('core:orders')

    def get_form(self, *args, **kwargs):
        form = super(OrderCreate, self).get_form(*args, **kwargs)
        form.fields['customer'].queryset = Customer.objects.all()
        return form

    def get_success_url(self):
        return reverse('core:order-detail', kwargs={'pk': self.object.id})


class OrderDetailView(DetailView):
    model = Order
    template_name = 'core/order.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['order_product_list'] = OrderProduct.objects.filter(order_id=self.get_object().id)
        return context


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('core:orders')


class OrderProductCreate(CreateView):
    model = OrderProduct
    fields = ['product', 'quantity']

    def form_valid(self, form):
        form.instance.order = Order.objects.get(id=self.kwargs['pk'])
        return super(OrderProductCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('core:order-detail', kwargs={'pk': pk})


class OrderProductUpdate(UpdateView):
    model = OrderProduct
    fields = ['product', 'quantity']

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('core:order-detail', kwargs={'pk': pk})

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        order_id = self.kwargs['pk']
        order_product_id = self.kwargs['opk']

        order = Order.objects.get(id=order_id)
        queryset = OrderProduct.objects.get(order_id=order_id, id=order_product_id)

        if not queryset or not order:
            raise Http404

        return queryset


class OrderProductDelete(DeleteView):
    model = OrderProduct

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        order_id = self.kwargs['pk']
        order_product_id = self.kwargs['opk']

        order = Order.objects.get(id=order_id)
        queryset = OrderProduct.objects.get(order_id=order_id, id=order_product_id)

        if not queryset or not order:
            raise Http404

        context = {
            'order': order,
            'product': queryset
        }

        return context

    def delete(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order_product_id = self.kwargs['opk']

        order_product = OrderProduct.objects.filter(order_id=order_id, id=order_product_id)
        order_product.delete()

        return HttpResponseRedirect(reverse('core:order-detail', kwargs={'pk': order_id}))
