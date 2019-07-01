from django.conf.urls import url
from django.urls import path, include

from users import views

urlpatterns = [
    path('logout/', views.logout_user, name='logout_user'),
]
