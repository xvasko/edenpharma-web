from django.urls import path

from .views import api_detail_customer_view, api_delete_customer_view, api_create_customer_view, \
    api_update_customer_view, api_accounts_login_view, ApiCustomerListView

app_name = 'api'

urlpatterns = [
    path('accounts/login', api_accounts_login_view, name='account-login'),
    path('customers', ApiCustomerListView.as_view(), name='customers'),
    path('customer/create', api_create_customer_view, name='customer-create'),
    path('customer/<int:pk>/', api_detail_customer_view, name='customer-detail'),
    path('customer/<int:pk>/update', api_update_customer_view, name='customer-update'),
    path('customer/<int:pk>/delete', api_delete_customer_view, name='customer-delete'),

]