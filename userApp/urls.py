from django.urls import path
from . import views

# All urls are at /user

urlpatterns = [
    path('login/', views.login),
    path('reg/', views.reg),
]