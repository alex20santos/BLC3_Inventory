import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from BLC3_Inventory import settings
from inventory.decorators import admin_required
from inventory.filters import ProductsFilter, OutputMovementFilter,InputMovementFilter
from inventory.forms import OutputModelFormset, InputModelFormset
from inventory.models import Product, OutputMovement, InputMovement
import xlrd
from django.contrib import messages

from reagents.models import ReagentGroup, Reagent
from users.models import Profile
import collections


#List all products. Hidden products included for admin
class AllProducts(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'all_product_list'
    template_name = 'inventory/product_list.html'
    queryset = Product.objects.all().order_by('name')
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_products'
        context['filter_form'] = ProductsFilter(self.request.GET, queryset=Product.objects.all()).form
        return context

    def get_queryset(self):
        if self.request.user.profile.is_admin:
            queryset = Product.objects.all().order_by('name')
        else:
            queryset = Product.objects.all().filter(is_active=True).order_by('name')
        return ProductsFilter(self.request.GET, queryset=queryset).qs


@method_decorator([login_required, admin_required, ], name='dispatch')
class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'inventory/create_product.html'
    fields = ['name','actual_quantity','material','capacity','location','brand','obs','reference','min_limit','is_active']
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_products'
        return context

    def form_valid(self, form):
        return super(ProductCreate, self).form_valid(form)


#Function to send email to all admins when minimum limit is reached
def notify_admins_low_stock(product,product_or_reagent):
    admins = Profile.objects.all().filter(is_admin=True)
    for a in admins:
        print(a.user.email)
        message = 'Caro(a) ' +a.user.first_name +' '+ a.user.last_name + ', este email serve para informar que o ' +\
             product_or_reagent+" " + product.name + ' atingiu o limite mínimo definido.' + '' \
               '\nCumprimentos, Inventário BLC3'

        send_mail(
            'Stock de '+product.name,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [a.user.email,],
            fail_silently = False,
            )


#Create output for a product or more
@login_required()
def create_output(request, product_id=None):
    template_name = 'inventory/remove_stock.html'

    if request.method == 'GET':
        if product_id is None:
            formset = OutputModelFormset(queryset=OutputMovement.objects.none())
        else:
            formset = OutputModelFormset(initial=[{'product': product_id,'quantity': 0,}],queryset= OutputMovement.objects.none())

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
                    succ_message =  'Saída de stock efetuada com sucesso no produto ' + product_obj.name
                    messages.success(request,succ_message)

                    # just to notify
                    if product_obj.actual_quantity <= product_obj.min_limit and product_obj.is_under_limit is False and product_obj.is_active:
                        notify_admins_low_stock(product_obj,'produto')
                        product_obj.is_under_limit = True
                        product_obj.save()

                else:
                    warn_message =  'Não foi possível registar a saída de stock de ' + product_obj.name
                    messages.warning(request,warn_message)
                form.save()
            return redirect('all_products_list')

    return render(request, template_name, {
        'formset': formset,
        'active_page': 'stock_output',
    })


@login_required()
@admin_required()
def create_input(request,product_id=None):
    template_name = 'inventory/add_stock.html'

    if request.method == 'GET':
        if product_id is None:
            formset = InputModelFormset(queryset=InputMovement.objects.none())
        else:
            formset = InputModelFormset(initial=[{'product': product_id,'quantity': 0,}],queryset= InputMovement.objects.none())

    elif request.method == 'POST':
        formset = InputModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                form.instance.user = request.user
                quantity = form.cleaned_data.get('quantity')
                product = form.cleaned_data.get('product')
                product_obj = Product.objects.get(id=product.id)
                product_obj.actual_quantity = product_obj.actual_quantity + quantity

                # update is_under_limit value
                if product_obj.actual_quantity > product_obj.min_limit and product_obj.is_under_limit is True and product_obj.is_active:
                    product_obj.is_under_limit = False

                product_obj.save()
                form.save()
                succ_message =  'Entrada de stock efetuada com sucesso no produto ' + product_obj.name
                messages.success(request,succ_message)
            return redirect('all_products_list')

    return render(request, template_name, {
        'formset': formset,
        'active_page': 'stock_input',
    })


#Read excel file with inventory table
def readExcelProducts():
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

def readExcelReagents():
    #https://stackoverflow.com/questions/24391892/printing-subscript-in-python
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    loc = ("reagentes.xlsx")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    v = []
    unit = 0

    for i in range(1,sheet.nrows):
        for j in range(sheet.ncols):
            if j == 0:
                group_name = sheet.cell_value(i, j)
            elif j == 7 or j==8:
                value = sheet.cell_value(i, j)
                result = re.findall(r'[A-Za-z]+|\d+', value)
                if j==7:
                    if result[-1] == 'g':
                        unit = 1
                    elif result[-1] == 'mL':
                        unit = 2
                    elif result[-1] == 'uni':
                        unit = 3
                    elif result[-1] == 'comp':
                        unit = 4
                    elif result[-1] == 'amp':
                        unit = 5
                    else:
                        unit = 0
                v.append(result[0])

            elif j== 9:
                v.append(sheet.cell_value(i, j).translate(SUB))
            else:
                v.append(sheet.cell_value(i, j))

        group = ReagentGroup.objects.all().filter(name__exact=group_name)
        r = Reagent.create(group[0],v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9],v[10],10,unit)
        r.save()
        v.clear()

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

@method_decorator([login_required, admin_required, ], name='dispatch')
class EditProduct(LoginRequiredMixin, UpdateView):
    model = Product
    fields =['name','material','capacity','location','brand','obs','reference','min_limit','is_active']
    template_name = 'inventory/update_product.html'
    success_url = "/inventory/all_products/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_products'
        return context

@method_decorator([login_required, admin_required, ], name='dispatch')
class AllOutputMovements(LoginRequiredMixin, ListView):
    model = OutputMovement
    context_object_name = 'all_output_movements'
    template_name = 'inventory/output_history.html'
    queryset = OutputMovement.objects.all().order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'history'
        context['active_sub_page'] = 'output_history'
        context['filter_form'] = OutputMovementFilter(self.request.GET, queryset=OutputMovement.objects.all()).form
        return context

    def get_queryset(self):
        queryset = OutputMovement.objects.all().order_by('-date')
        return OutputMovementFilter(self.request.GET, queryset=queryset).qs

@method_decorator([login_required, admin_required, ], name='dispatch')
class AllInputMovements(LoginRequiredMixin, ListView):
    model = InputMovement
    context_object_name = 'all_input_movements'
    template_name = 'inventory/input_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'history'
        context['active_sub_page'] = 'input_history'
        context['filter_form'] = InputMovementFilter(self.request.GET, queryset=InputMovement.objects.all()).form
        return context

    def get_queryset(self):
        queryset = InputMovement.objects.all().order_by('-date')
        return InputMovementFilter(self.request.GET, queryset=queryset).qs
