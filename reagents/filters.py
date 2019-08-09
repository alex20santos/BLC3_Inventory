import django_filters
from django.contrib.auth.models import User

from inventory.models import Product, OutputMovement, InputMovement


class ReagentsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Nome do produto')
    location = django_filters.CharFilter(lookup_expr='icontains', label='Localização')
    reference = django_filters.CharFilter(lookup_expr='icontains', label='Referência')

    class Meta:
        model = Product
        fields = ['name', 'reference','location' ]



class OutputMovementReagentFilter(django_filters.FilterSet):
    date = django_filters.DateRangeFilter(label='Data')

    class Meta:
        model = OutputMovement
        fields = ['date','user']

    def __init__(self, *args, **kwargs):
        super(OutputMovementReagentFilter, self).__init__(*args, **kwargs)
        self.filters['user'].queryset = User.objects.filter().all()


class InputMovementReagentFilter(django_filters.FilterSet):
    date = django_filters.DateRangeFilter(label='Data')

    class Meta:
        model = InputMovement
        fields = ['date','user']

    def __init__(self, *args, **kwargs):
        super(InputMovementReagentFilter, self).__init__(*args, **kwargs)
        self.filters['user'].queryset = User.objects.filter().all()