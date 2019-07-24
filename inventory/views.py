from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from inventory.decorators import admin_required
from inventory.filters import ProductsFilter
from inventory.forms import OutputModelFormset, InputModelFormset
from inventory.models import Product, OutputMovement, InputMovement


class AllProducts(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'all_product_list'
    template_name = 'inventory/product_list.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_products'
        context['filter_form'] = ProductsFilter(self.request.GET, queryset=Product.objects.all()).form
        return context

    def get_queryset(self):
        queryset = Product.objects.all()
        return ProductsFilter(self.request.GET, queryset=queryset).qs


@method_decorator([login_required, admin_required, ], name='dispatch')
class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'inventory/create_product.html'
    fields = '__all__'
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_products'
        return context

    def form_valid(self, form):
        return super(ProductCreate, self).form_valid(form)


@login_required()
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
                product_obj = Product.objects.get(id=product.id)
                if product_obj.actual_quantity - quantity >= 0:
                    product_obj.actual_quantity = product_obj.actual_quantity - quantity
                    product_obj.save()
                form.save()
                return redirect('all_products_list')

    return render(request, template_name, {
        'formset': formset,
        'active_page': 'stock_output',
    })


@login_required()
@admin_required()
def create_input(request):
    template_name = 'inventory/add_stock.html'

    if request.method == 'GET':
        formset = InputModelFormset(queryset=InputMovement.objects.none())

    elif request.method == 'POST':
        formset = InputModelFormset(request.POST)

        if formset.is_valid():
            for form in formset:
                form.instance.user = request.user
                quantity = form.cleaned_data.get('quantity')
                product = form.cleaned_data.get('product')
                product_obj = Product.objects.get(id=product.id)
                product_obj.actual_quantity = product_obj.actual_quantity + quantity
                product_obj.save()
                form.save()
                return redirect('all_products_list')

    return render(request, template_name, {
        'formset': formset,
        'active_page': 'stock_input',
    })


##READ excel files
'''
import xlrd
# Give the location of the file
loc = ("simple_inv.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

values_to_insert = [None for _ in range(10)]
for i in range(sheet.nrows):
    for j in range(sheet.ncols):
        if j == 7 :
            values_to_insert[j-1] += sheet.cell_value(i, j)
        else:
            values_to_insert[j] = sheet.cell_value(i, j)
    p = Product.create(values_to_insert[0],values_to_insert[1],values_to_insert[2],values_to_insert[3],
        values_to_insert[4],values_to_insert[5],values_to_insert[6],values_to_insert[8],values_to_insert[9])
    p.save() 
'''

class ProductDetails(LoginRequiredMixin, DetailView):
    model = Product
    fields = '__all__'

    def get_context_data(self, **kwargs):
        product_id = self.kwargs.get('pk')
        product = Product.objects.get(pk=product_id)
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_products'
        context['product_id'] = product.id,
        return context


class EditProduct(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'inventory/update_product.html'
    success_url = "/inventory/all_products/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_products'
        return context