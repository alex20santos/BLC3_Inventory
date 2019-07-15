from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from inventory.decorators import admin_required
from inventory.forms import OutputModelFormset
from inventory.models import Product, OutputMovement


class AllProducts(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'all_product_list'
    template_name = 'inventory/product_list.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_products'

        return context

@method_decorator([login_required, admin_required, ], name='dispatch')
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

@login_required()
@admin_required()
def create_output(request):
    template_name = 'inventory/remove_stock.html'

    if request.method == 'GET':
        formset = OutputModelFormset(queryset=OutputMovement.objects.none())

    elif request.method == 'POST':
        formset = OutputModelFormset(request.POST)

        if formset.is_valid():
            for form in formset:
                form.instance.user = request.user
                quantity = form.cleaned_data.get('quantity')
                product = form.cleaned_data.get('product')
                product_obj = Product.objects.get(id = product.id)
                if product_obj.actual_quantity - quantity >= 0:
                    product_obj.actual_quantity = product_obj.actual_quantity - quantity
                    product_obj.save()
                form.save()
                return redirect('home')

    return render(request, template_name, {
        'formset': formset,
        'active_page':'stock_output',
    })

@login_required()
@admin_required()
def create_input(request):
    template_name = 'inventory/add_stock.html'

    if request.method == 'GET':
        formset = OutputModelFormset(queryset=OutputMovement.objects.none())

    elif request.method == 'POST':
        formset = OutputModelFormset(request.POST)

        if formset.is_valid():
            for form in formset:
                form.instance.user = request.user
                quantity = form.cleaned_data.get('quantity')
                product = form.cleaned_data.get('product')
                product_obj = Product.objects.get(id = product.id)
                product_obj.actual_quantity = product_obj.actual_quantity + quantity
                product_obj.save()
                form.save()
                return redirect('home')

    return render(request, template_name, {
        'formset': formset,
        'active_page':'stock_input',
    })