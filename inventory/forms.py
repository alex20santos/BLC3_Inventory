from django import forms

from inventory.models import OutputMovement, InputMovement, Product
from django.forms.models import modelformset_factory


class OutputModelForm(forms.ModelForm):
    class Meta:
        model = OutputMovement
        fields = ('product', 'quantity',)

    def __init__(self, *args, **kwargs):
        super(OutputModelForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True)

class InputModelForm(forms.ModelForm):
    class Meta:
        model = InputMovement
        fields = ('product', 'quantity',)

    def __init__(self, *args, **kwargs):
        super(InputModelForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True)

OutputModelFormset = modelformset_factory(
    OutputMovement,
    form=OutputModelForm,
    fields=('product', 'quantity',),
    extra=1,

)

InputModelFormset = modelformset_factory(
    InputMovement,
    form=InputModelForm,
    fields=('product', 'quantity',),
    extra=1,
)
