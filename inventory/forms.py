from django import forms

from inventory.models import OutputMovement, InputMovement
from django.forms.models import modelformset_factory


class OutputModelForm(forms.ModelForm):
    class Meta:
        model = OutputMovement
        fields = ('product', 'quantity',)


class InputModelForm(forms.ModelForm):
    class Meta:
        model = InputMovement
        fields = ('product', 'quantity',)


OutputModelFormset = modelformset_factory(
    OutputMovement,
    fields=('product', 'quantity',),
    extra=1,
)

InputModelFormset = modelformset_factory(
    InputMovement,
    fields=('product', 'quantity',),
    extra=1,
)
