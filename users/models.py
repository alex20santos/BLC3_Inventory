from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(verbose_name=_('Admin'), default=False)

    def __str__(self):
        return str(self.user.first_name) +" "+ self.user.last_name