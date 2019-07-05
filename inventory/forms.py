
from django import forms

from inventory.models import Product, OutputMovement, Movement
from django.forms.models import inlineformset_factory
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from crispy_forms.helper import FormHelper
from .custom_layout_object import *


class OutputMovementForm(forms.ModelForm):

    class Meta:
        model = OutputMovement
        exclude = ()

class MovementForm(forms.ModelForm):

    class Meta:
        model = Movement
        exclude = ['created_by', ]

    def __init__(self, *args, **kwargs):
        super(MovementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Div(
                Fieldset('',Formset('movements')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Guardar')),
            )
        )

MovementFormSet = inlineformset_factory(
    Movement, OutputMovement, form=OutputMovementForm,
    fields=['product','quantity',], extra=1, can_delete=True
)

