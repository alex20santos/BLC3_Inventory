from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from inventory.views import AllProducts

urlpatterns = [
    path('all_products/', AllProducts.as_view(), name='all_products_list'),

]