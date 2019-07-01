from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


MOVEMENT_OPTIONS =(
    (0, _('Saída')),
    (1, _('Entrada')),
)

UNIT_CHOICES =(
    (0,"N/A"),
    (1,"L"),
    (2,"Kg"),
    (3,"m"),
)

class Product(models.Model):
    class Meta:
        verbose_name = _('Produto')
    name = models.CharField(max_length=300,verbose_name=_('Nome'))
    actual_quantity  = models.IntegerField(verbose_name=_("quantidade atual"))
    unit = models.IntegerField(verbose_name=_('unidade'), choices=UNIT_CHOICES, default=0)

    def __str__(self):
        return self.name

class Movement(models.Model):
    class Meta:
        verbose_name = _('Movimentação')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True,verbose_name=_('produto'))
    quantity  = models.IntegerField(verbose_name=_("quantidade"))
    user = models.ForeignKey(User,on_delete=models.CASCADE,to_field='id',verbose_name=_('utilizador'))
    movement_type = models.IntegerField(verbose_name=_('tipo de movimento'), choices=MOVEMENT_OPTIONS, default=0) # 0-> saída, 1-> entrada


