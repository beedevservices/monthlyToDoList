from django.contrib import admin
from django.urls import path, include
from userApp import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('userApp.urls')),
]
