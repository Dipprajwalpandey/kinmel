from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='StoreHome'),
    path('search/', views.search, name='Search'),
    path('about/', views.about, name='AboutUs'),
    path('contact/', views.contact, name='ContactUs'),
    path('tracker/', views.tracker, name='TrackingStatus'),
    path('products/<int:myid>/', views.productView, name='ProductView'),
    path('checkout/', views.checkout, name='Checkout'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('esewa/success/', views.esewa_success, name='EsewaSuccess'),
    path('esewa/failure/', views.esewa_failure, name='EsewaFailure'),
    path('deals/', views.deals, name='Deals'),
    path('new-arrivals/', views.new_arrivals, name='NewArrivals'),
    path('brands/', views.brands, name='Brands'),
    path('support/', views.support, name='Support'),
    path('category/<str:category_name>/', views.category, name='Category'),
    path('reports/', views.reports, name='Reports'),
]