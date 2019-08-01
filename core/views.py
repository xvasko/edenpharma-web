from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
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


class OverviewView(LoginRequiredMixin, TemplateView):
    context_object_name = 'context'
    template_name = 'core/overview.html'

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()

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


class ProductView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'core/products.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'core/product.html'

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'price']
    success_url = reverse_lazy('core:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        return context


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['title', 'price']

    def get_success_url(self):
        return reverse('core:product-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = False
        return context


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('core:products')


class CustomerView(LoginRequiredMixin,ListView):
    model = Customer
    template_name = 'core/customers.html'


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'core/customer.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(customer_id=self.kwargs['pk'])
        return context


class CustomerCreate(LoginRequiredMixin,CreateView):
    model = Customer
    fields = ['name', 'city', 'street', 'zip', 'phone_number']
    success_url = reverse_lazy('core:customers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        return context


class CustomerUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ['name', 'city', 'street', 'zip', 'phone_number']

    def get_success_url(self):
        return reverse('core:customer-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = False
        return context


class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('core:customers')


# ============================
class OrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'core/orders.html'


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['customer']

    def get_form(self, *args, **kwargs):
        form = super(OrderCreate, self).get_form(*args, **kwargs)
        form.fields['customer'].queryset = Customer.objects.all()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OrderCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('core:order-detail', kwargs={'pk': self.object.id})


from django.utils import timezone


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'core/order.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        created_at = Order.objects.get(id=self.kwargs['pk']).created_at
        if created_at is not None:
            context['created_at_formatted'] = timezone.localtime(created_at).strftime("%d.%m.%Y %H:%M")
        else:
            context['created_at_formatted'] = None
        context['order_product_list'] = OrderProduct.objects.filter(order_id=self.get_object().id)
        return context


class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('core:orders')


class OrderProductCreate(LoginRequiredMixin, CreateView):
    model = OrderProduct
    fields = ['product', 'quantity']

    def form_valid(self, form):
        form.instance.order = Order.objects.get(id=self.kwargs['pk'])
        return super(OrderProductCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('core:order-detail', kwargs={'pk': pk})


class OrderProductUpdate(LoginRequiredMixin, UpdateView):
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


class OrderProductDelete(LoginRequiredMixin, DeleteView):
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
