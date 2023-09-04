from django.shortcuts import render, redirect
from django.contrib import messages
from userApp.models import *

def profile(request):
    if 'user_id' not in request.session:
        messages.error(request, "you need to be logged in to view this page")
        return redirect('/logReg/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        theUser = user.firstName
        context = {
            'user': user,
        }
        return render(request, 'profile.html', context)
    
def updateEmail(request):
    pass

def updatePassword(request):
    pass

def requestPassword(request):
    pass