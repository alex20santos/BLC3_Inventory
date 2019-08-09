from django import forms
from django.forms import modelformset_factory

from reagents.models import Reagent, OutputMovementReagent, InputMovementReagent


class OutputModelFormReagent(forms.ModelForm):
    class Meta:
        model = OutputMovementReagent
        fields = ('reagent', 'quantity',)

    def __init__(self, *args, **kwargs):
        super(OutputModelFormReagent, self).__init__(*args, **kwargs)
        self.fields['reagent'].queryset = Reagent.objects.filter(is_active=True)


class InputModelFormReagent(forms.ModelForm):
    class Meta:
        model = InputMovementReagent
        fields = ('reagent', 'quantity',)

    def __init__(self, *args, **kwargs):
        super(InputModelFormReagent, self).__init__(*args, **kwargs)
        self.fields['reagent'].queryset = Reagent.objects.filter(is_active=True)

OutputModelFormset = modelformset_factory(
    OutputMovementReagent,
    form=OutputModelFormReagent,
    fields=('reagent', 'quantity',),
    extra=1,

)


InputModelFormset = modelformset_factory(
    InputMovementReagent,
    form=InputModelFormReagent,
    fields=('reagent', 'quantity',),
    extra=1,
)
