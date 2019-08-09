from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.



#List all products. Hidden products included for admin
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DetailView

from inventory.decorators import admin_required
from inventory.views import notify_admins_low_stock
from reagents.filters import ReagentsFilter, OutputMovementReagentFilter, InputMovementReagentFilter
from reagents.forms import OutputModelFormset, InputModelFormset
from reagents.models import Reagent, OutputMovementReagent, InputMovementReagent


class AllReagents(LoginRequiredMixin, ListView):
    model = Reagent
    context_object_name = 'all_reagents_list'
    template_name = 'reagents/reagents_list.html'
    queryset = Reagent.objects.all().order_by('name')
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_reagents'
        context['filter_form'] = ReagentsFilter(self.request.GET, queryset=Reagent.objects.all()).form
        return context

    def get_queryset(self):
        if self.request.user.profile.is_admin:
            queryset = Reagent.objects.all().order_by('name')
        else:
            queryset = Reagent.objects.all().filter(is_active=True).order_by('name')
        return ReagentsFilter(self.request.GET, queryset=queryset).qs


@method_decorator([login_required, admin_required, ], name='dispatch')
class EditReagent(LoginRequiredMixin, UpdateView):
    model = Reagent
    fields =['name','name_en','location','grade','number','group','package_quantity','unit',
             'n_cas','formula','manufacturer','reference','min_limit','is_active']

    template_name = 'reagents/update_reagent.html'
    success_url = "/reagents/all_reagents/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_reagents'
        return context



#Create output for a product or more
@login_required()
def create_output(request, reagent_id=None):
    template_name = 'reagents/remove_stock.html'

    if request.method == 'GET':
        if reagent_id is None:
            formset = OutputModelFormset(queryset=OutputMovementReagent.objects.none())
        else:
            formset = OutputModelFormset(initial=[{'reagent': reagent_id,'quantity': 0,}],queryset= OutputMovementReagent.objects.none())

    elif request.method == 'POST':
        formset = OutputModelFormset(request.POST)

        if formset.is_valid():
            for form in formset:
                form.instance.user = request.user
                quantity = form.cleaned_data.get('quantity')
                reagent = form.cleaned_data.get('reagent')
                reagent_obj = Reagent.objects.get(id=reagent.id)
                if reagent_obj.quantity - quantity >= 0:
                    reagent_obj.quantity = reagent_obj.quantity - quantity
                    reagent_obj.save()
                    succ_message =  'Saída de stock efetuada com sucesso no reagent ' + reagent_obj.name
                    messages.success(request,succ_message)

                    # just to notify
                    if reagent_obj.quantity <= reagent_obj.min_limit and reagent_obj.is_under_limit is False and reagent_obj.is_active:
                        notify_admins_low_stock(reagent_obj,"reagente")
                        reagent_obj.is_under_limit = True
                        reagent_obj.save()

                else:
                    warn_message =  'Não foi possível registar a saída de stock de ' + reagent_obj.name
                    messages.warning(request,warn_message)
                form.save()
            return redirect('all_reagents_list')

    return render(request, template_name, {
        'formset': formset,
        'active_page': 'stock_output_reagents',
    })



@login_required()
@admin_required()
def create_input(request,reagent_id=None):
    template_name = 'reagents/add_stock.html'

    if request.method == 'GET':
        if reagent_id is None:
            formset = InputModelFormset(queryset=InputMovementReagent.objects.none())
        else:
            formset = InputModelFormset(initial=[{'reagent': reagent_id,'quantity': 0,}],queryset= InputMovementReagent.objects.none())

    elif request.method == 'POST':
        formset = InputModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                form.instance.user = request.user
                quantity = form.cleaned_data.get('quantity')
                reagent = form.cleaned_data.get('reagent')
                reagent_obj = Reagent.objects.get(id=reagent.id)
                reagent_obj.quantity = reagent_obj.quantity + quantity

                # update is_under_limit value
                if reagent_obj.quantity > reagent_obj.min_limit and reagent_obj.is_under_limit is True and reagent_obj.is_active:
                    reagent_obj.is_under_limit = False

                reagent_obj.save()
                form.save()
                succ_message =  'Entrada de stock efetuada com sucesso no reagente ' + reagent_obj.name
                messages.success(request,succ_message)
            return redirect('all_reagents_list')

    return render(request, template_name, {
        'formset': formset,
        'active_page': 'stock_input_reagents',
    })




@method_decorator([login_required, admin_required, ], name='dispatch')
class AllOutputMovements(LoginRequiredMixin, ListView):
    model = OutputMovementReagent
    context_object_name = 'all_output_movements_reagents'
    template_name = 'reagents/output_history.html'
    queryset = OutputMovementReagent.objects.all().order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'history_reagents'
        context['active_sub_page'] = 'output_history_reagents'
        context['filter_form'] = OutputMovementReagentFilter(self.request.GET, queryset=OutputMovementReagent.objects.all()).form
        return context

    def get_queryset(self):
        queryset = OutputMovementReagent.objects.all().order_by('-date')
        return OutputMovementReagentFilter(self.request.GET, queryset=queryset).qs

@method_decorator([login_required, admin_required, ], name='dispatch')
class AllInputMovements(LoginRequiredMixin, ListView):
    model = InputMovementReagent
    context_object_name = 'all_input_movements_reagents'
    template_name = 'reagents/input_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'history_reagents'
        context['active_sub_page'] = 'input_history_reagents'
        context['filter_form'] = InputMovementReagentFilter(self.request.GET, queryset=InputMovementReagent.objects.all()).form
        return context

    def get_queryset(self):
        queryset = InputMovementReagent.objects.all().order_by('-date')
        return InputMovementReagentFilter(self.request.GET, queryset=queryset).qs




@method_decorator([login_required, admin_required, ], name='dispatch')
class ReagentCreate(LoginRequiredMixin, CreateView):
    model = Reagent
    template_name = 'reagents/create_reagent.html'
    fields = ['name','name_en','location','grade','number','group','quantity','package_quantity','n_cas',
              'formula','manufacturer','reference','unit','min_limit','is_active']
    success_url = "/reagents/all_reagents"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_reagents'
        return context

    def form_valid(self, form):
        return super(ReagentCreate, self).form_valid(form)



class ReagentDetails(LoginRequiredMixin, DetailView):
    model = Reagent
    fields = '__all__'

    def get_context_data(self, **kwargs):
        reagent_id = self.kwargs.get('pk')
        product = Reagent.objects.get(pk=reagent_id)
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'all_reagents'
        context['reagent_id'] = product.id,
        return context