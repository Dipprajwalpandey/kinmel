from django.urls import path
from . import views

urlpatterns = [
    # The home page of your blog
    path('', views.index, name='blogHome'),

    # The dynamic path for individual posts
    # The <int:id> part matches the 'id' argument in your blogpost view
    path('blogpost/<int:id>/', views.blogpost, name='blogPost'),
]