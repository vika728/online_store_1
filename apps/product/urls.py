from django.urls import path

from apps.product.views import *

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('product/products_list/', ProductListView.as_view(), name='products-list'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/edit/<int:pk>/', ProductEditView.as_view(), name='product-edit'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/review/<int:pk>/', ReviewIndexPage.as_view(), name='review-list'),
    path('products/review-create/', ReviewCreate.as_view(), name='review-create'),
]