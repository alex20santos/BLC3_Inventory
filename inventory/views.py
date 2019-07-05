from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from inventory.forms import MovementForm, MovementFormSet, OutputMovementForm
from inventory.models import Product, Movement, OutputMovement


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



class RemoveStock(LoginRequiredMixin,CreateView):
    model = Movement
    template_name = 'inventory/remove_stock.html'

    fields = '__all__'

    def form_valid(self, form):
        return super(RemoveStock, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'stock_output'
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'homepage'},
        ]
        return context




class OutputMovementCreate(LoginRequiredMixin, CreateView):
    model = Movement
    template_name = 'inventory/remove_stock.html'
    form_class = MovementForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        data = super(OutputMovementCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['movements'] = MovementFormSet(self.request.POST)
        else:
            data['movements'] = MovementFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        movements = context['movements']
        with transaction.atomic():
            form.instance.user = self.request.user
            print(form.instance.user)
            self.object = form.save()
            if movements.is_valid():
                movements.instance = self.object
                movements.save()

        return super(OutputMovementCreate, self).form_valid(form)


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'inventory/create_product.html'
    fields = '__all__'
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return super(ProductCreate, self).form_valid(form)