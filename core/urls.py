from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path, include
from . import views
from .views import ProductView, ProductDetailView, CustomerView, OrderView, OrderDetailView, ProductCreate, \
    ProductUpdate, ProductDelete, CustomerCreate, CustomerDetailView, CustomerUpdate, CustomerDelete, OrderCreate, \
    OrderProductDelete, OrderProductCreate, OrderDelete, OrderProductUpdate, OverviewView

app_name = 'core'

urlpatterns = [
    path('api/', include('api.urls', 'api')),

    path('', ProductView.as_view(), name='index'),
    path('overview/', OverviewView.as_view(), name='overview'),


    path('products/', ProductView.as_view(), name='products'),
    path('product/create/', ProductCreate.as_view(), name='product-create'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update', ProductUpdate.as_view(), name='product-update'),
    path('product/<int:pk>/delete', ProductDelete.as_view(), name='product-delete'),

    path('customers/', CustomerView.as_view(), name='customers'),
    path('customer/create/', CustomerCreate.as_view(), name='customer-create'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('customer/<int:pk>/update', CustomerUpdate.as_view(), name='customer-update'),
    path('customer/<int:pk>/delete', CustomerDelete.as_view(), name='customer-delete'),

    path('orders/', OrderView.as_view(), name='orders'),
    path('order/create/', OrderCreate.as_view(), name='order-create'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order/<int:pk>/delete', OrderDelete.as_view(), name='order-delete'),

    path('order/<int:pk>/order-product/create', OrderProductCreate.as_view(), name='order-product-create'),
    path('order/<int:pk>/order-product/<int:opk>/update', OrderProductUpdate.as_view(), name='order-product-update'),
    path('order/<int:pk>/order-product/<int:opk>/delete', OrderProductDelete.as_view(), name='order-product-delete'),

]
