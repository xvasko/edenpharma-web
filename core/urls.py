from django.urls import path
from . import views
from .views import ProductView, ProductDetailView, customers, OrderView, OrderDetailView

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', ProductView.as_view(), name='products'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product'),
    path('customers/', customers, name='customers'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('orders/<slug>', OrderDetailView.as_view(), name='order'),
]
