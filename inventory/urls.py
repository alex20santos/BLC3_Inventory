from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from inventory.views import AllProducts, ProductCreate, create_output, create_input, ProductDetails, EditProduct, \
    AllOutputMovements, AllInputMovements

urlpatterns = [
    path('all_products/', AllProducts.as_view(), name='all_products_list'),
    path('new_product/', ProductCreate.as_view(), name='product_create'),
    path('remove_stock/', create_output, name='remove_stock'),
    path('remove_stock/<int:product_id>', create_output, name='remove_stock'),
    path('add_stock/', create_input, name='add_stock'),
    path('add_stock/<int:product_id>', create_input, name='add_stock'),
    path('product_details/<int:pk>', ProductDetails.as_view(), name='product_details'),
    path('product_edit/<int:pk>', EditProduct.as_view(), name='product_edit'),
    path('output_history/', AllOutputMovements.as_view(), name='output_history'),
    path('input_history/', AllInputMovements.as_view(), name='input_history'),

]