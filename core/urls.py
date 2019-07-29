from django.urls import path
from . import views
from .views import ProductView, ProductDetailView, CustomerView, OrderView, OrderDetailView, ProductCreate, \
    ProductUpdate, ProductDelete, CustomerCreate, CustomerDetailView, CustomerUpdate, CustomerDelete

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
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
    path('orders/<slug>', OrderDetailView.as_view(), name='order')
]