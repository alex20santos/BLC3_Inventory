from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


MOVEMENT_OPTIONS =(
    (0, _('Saída')),
    (1, _('Entrada')),
)


class Product(models.Model):
    class Meta:
        verbose_name = _('Produto')
    name = models.CharField(max_length=300,verbose_name=_('Nome'))
    actual_quantity = models.PositiveIntegerField(verbose_name=_("quantidade atual"))
    material = models.CharField(max_length=300, verbose_name=_('material'))
    capacity = models.CharField(max_length=300, verbose_name=_('capacidade/comprimento'))
    location = models.CharField(max_length=300, verbose_name=_('localização'))
    brand = models.CharField(max_length=300, verbose_name=_('marca'))
    obs = models.TextField(verbose_name=_('observações'))
    reference = models.CharField(max_length=300, verbose_name=_('referência'))
    min_limit  = models.IntegerField(verbose_name=_("limite mínimo"))

    def __str__(self):
        return self.name


class Movement(models.Model):
    class Meta:
        verbose_name = _('Movimentação')

    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "movement : " +  str(self.id)

class OutputMovement(models.Model):
    class Meta:
        verbose_name = _('Movimentação Saída')

    movement = models.ForeignKey(Movement, on_delete=models.CASCADE,blank=True,verbose_name=_('movimentação'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True,verbose_name=_('produto'))
    quantity  = models.PositiveIntegerField(verbose_name=_("quantidade"))

    def __str__(self):
        return "output movement : " +  str(self.product)





