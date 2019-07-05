from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from inventory.views import AllProducts, RemoveStock, OutputMovementCreate, ProductCreate

urlpatterns = [
    path('all_products/', AllProducts.as_view(), name='all_products_list'),
    path('new_product/', ProductCreate.as_view(), name='product_create'),
    path('remove_stock/', OutputMovementCreate.as_view(), name='remove_stock'),

]