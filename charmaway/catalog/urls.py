from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_list, name='category'),
    path('brand/<int:brand_id>/', views.brand_list, name='brand'),
]
