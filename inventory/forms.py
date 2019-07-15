
from django import forms

from inventory.models import OutputMovement
from django.forms.models import modelformset_factory



class OutputModelForm(forms.ModelForm):

    class Meta:
        model = OutputMovement
        fields = ('product','quantity', )



OutputModelFormset = modelformset_factory(
    OutputMovement,
    fields=('product','quantity', ),
    extra=1,
    labels = {
        #'product': '',
        #'quantity': ''
    }
)