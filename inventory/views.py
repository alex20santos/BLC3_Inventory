from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from inventory.models import Product


class AllProducts(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 3
    context_object_name = 'all_product_list'
    template_name = 'inventory/product_list.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_products'

        return context