from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token 

from . import views

urlpatterns = [
    path('auth/', obtain_auth_token),
    # path('auth/', admin.site.urls), # create an endpoint to genereate the tokens
    path('', views.api_home) #localhost/api/
]