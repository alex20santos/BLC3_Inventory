from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib import messages

# Create your views here.



''' 
view para fazer logout ao utilizador
'''
def logout_user(request):
    logout(request)
    return redirect("login")

