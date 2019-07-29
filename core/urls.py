from django.urls import path
from . import views
from .views import ProductView, ProductDetailView, customers, OrderView, OrderDetailView, ProductCreate, ProductUpdate, ProductDelete

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', ProductView.as_view(), name='products'),
    path('product/create/', ProductCreate.as_view(), name='product-create'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('product/<int:pk>/update', ProductUpdate.as_view(), name='product-update'),
    path('product/<int:pk>/delete', ProductDelete.as_view(), name='product-delete'),
    path('customers/', customers, name='customers'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('orders/<slug>', OrderDetailView.as_view(), name='order'),
]
