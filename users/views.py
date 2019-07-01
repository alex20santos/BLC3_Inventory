from django.contrib.auth import logout
from django.shortcuts import render, redirect

# Create your views here.



''' 
view para fazer logout ao utilizador
'''
def logout_user(request):
    logout(request)
    return redirect("login")