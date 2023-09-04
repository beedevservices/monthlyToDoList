from django.shortcuts import render, redirect
from django.contrib import messages
from coreApp.models import *
from userApp.models import *

def index(request):
    if 'user_id' not in request.session:
        user = False
    else:
        user = User.objects.get(id=request.session['user_id'])
    tasks = Task.objects.filter(user_id=request.session['user_id'])
    if not tasks:
        tasks = False
        context = {
            'user': user,
        }
        return render(request, 'index.html', contect)
    context = {
        'user': user,
        'tasks': tasks,
    }
    return render(request, 'dashboard.html', context)

def dashboard(request):
    pass

def logout(request):
    pass

