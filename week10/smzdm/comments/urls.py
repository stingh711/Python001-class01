from django.urls import path

from . import views


urlpatterns = [
    path("home/", views.home, name="home"),
    path("products/", views.list_products, name="list_products"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("comments/", views.list_comments, name="list_comments"),
]
