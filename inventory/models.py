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

    @classmethod
    def create(cls,name,material,capacity,actual_quantity,location,brand,obs,reference,min_limit ):
        print(name,material,capacity,actual_quantity,location,brand,obs,reference,min_limit)
        product = cls(name=name,material=material,capacity=capacity,actual_quantity=actual_quantity,location=location,brand=brand,obs=obs,reference=reference,min_limit=min_limit)
        return product


class OutputMovement(models.Model):
    class Meta:
        verbose_name = _('Movimentação Saída')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True,verbose_name=_('produto'))
    quantity  = models.PositiveIntegerField(null=True,verbose_name=_("quantidade"))

    def __str__(self):
        return "output movement : " +  str(self.product)


class InputMovement(models.Model):
    class Meta:
        verbose_name = _('Movimentação Entrada')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True,verbose_name=_('produto'))
    quantity  = models.PositiveIntegerField(null=True,verbose_name=_("quantidade"))

    def __str__(self):
        return "input movement : " +  str(self.product)





