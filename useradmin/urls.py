from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview_view, name='useradmin_overview'),
    path('add-products/', views.add_product_view, name='add_products'),
    path('reports/', views.reports_view, name='reports'),
    path('orders/', views.orders_view, name='useradmin_orders'),
]