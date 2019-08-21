import os

from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Create your models here.




class ReagentGroup(models.Model):
    class Meta:
        verbose_name = _('Grupo')
    name = models.CharField(max_length=300,verbose_name=_('Nome'))

    def __str__(self):
        return self.name

    @classmethod
    def create(cls,name ):
        reagent = cls(name=name)
        return reagent


UNIT_OPTIONS =(
    (0, _('Outro')),
    (1, _('g')),
    (2, _('mL')),
    (3, _('uni.')),
    (4, _('compr.')),
    (5, _('amp.')),
)

def get_upload_path(instance, filename):
    path_name = "reagents_files/"+instance.name+"/TDS"
    return os.path.join(path_name,filename)

def get_upload_path_sds(instance, filename):
    path_name = "reagents_files/"+instance.name+"/SDS"
    return os.path.join(path_name,filename)


class Reagent(models.Model):
    class Meta:
        verbose_name = _('Reagente')
    name = models.CharField(max_length=300,verbose_name=_('Nome'))
    name_en = models.CharField(max_length=300,verbose_name=_('Nome em inglês'))
    location = models.CharField(max_length=300,verbose_name=_('Localização'))
    grade = models.CharField(max_length=300,verbose_name=_('Grau'))
    number = models.CharField(max_length=30,verbose_name=_('Número'))
    group = models.ForeignKey(ReagentGroup, blank=False, null=True, on_delete=models.SET_NULL)
    quantity  = models.DecimalField(max_digits=100,decimal_places=3,null=True,validators=[MinValueValidator(Decimal('0.01'))],verbose_name=_("quantidade"))
    package_quantity = models.DecimalField(max_digits=100,decimal_places=3,null=True,verbose_name=_("Quandidade por embalagem"))
    n_cas = models.CharField(max_length=50,verbose_name=_('Número CAS'))
    formula = models.CharField(max_length=100,verbose_name=_('Fórmula'))
    manufacturer = models.CharField(max_length=300,verbose_name=_('Fabricante'))
    reference = models.CharField(max_length=300,verbose_name=_('Referência'))
    unit = models.IntegerField(verbose_name=_('Unidade'), choices=UNIT_OPTIONS, default=0)
    min_limit  = models.PositiveIntegerField(verbose_name=_("limite mínimo"))
    is_active = models.BooleanField(default=True,verbose_name=_("Visível"))
    is_under_limit = models.BooleanField(default=False)
    tds = models.FileField(upload_to=get_upload_path, blank=True, verbose_name=_('Ficha técnica (TDS)'))
    sds = models.FileField(upload_to=get_upload_path_sds, blank=True, verbose_name=_('Ficha técnica (SDS)'))


    @classmethod
    def create(cls,group,number,name,name_en,location,n_cas,grade,quantity,package_quantity,formula,manufacturer,reference,min_limit,unit ):
        reagent = cls(group=group,number=number,name=name,name_en=name_en,location=location,n_cas=n_cas,grade=grade,
                      quantity=quantity,package_quantity=package_quantity,formula=formula,manufacturer=manufacturer,
                      reference=reference,min_limit=min_limit,unit=unit )
        return reagent

    def __str__(self):
        return str(self.name) + ' ('+str(UNIT_OPTIONS[self.unit][1])+')'



class OutputMovementReagent(models.Model):
    class Meta:
        verbose_name = _('Movimentação Saída')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE,blank=True,verbose_name=_('reagente'))
    quantity  = models.DecimalField(max_digits=100,decimal_places=3,null=True,validators=[MinValueValidator(Decimal('0.01'))], verbose_name=_("quantidade"))
    date = models.DateTimeField(default=timezone.now,verbose_name=_('Data'))

    def __str__(self):
        return "output movement : " +  str(self.reagent.name)



class InputMovementReagent(models.Model):
    class Meta:
        verbose_name = _('Movimentação Entrada')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE,blank=True,verbose_name=_('reagente'))
    quantity  = models.DecimalField(max_digits=100,decimal_places=3,null=True,validators=[MinValueValidator(Decimal('0.01'))],verbose_name=_("quantidade"))
    date = models.DateTimeField(default=timezone.now,verbose_name=_('Data'))

    def __str__(self):
        return "input movement : " +  str(self.reagent)



