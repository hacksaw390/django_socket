from django.shortcuts import render, redirect
from .models import Group, Chat

# Create your views here.

def index(request, groupname):
    group = Group.objects.filter(name=groupname).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group= group)
    else:
        group = Group(name=groupname)
        group.save()
    context = {
        'groupname':groupname,
        'chats': chats
        }
    return render(request, 'chat/index.html',context)

def lobby(request):
    return render(request, 'home/home.html')


def home(request):
    return render(request, 'master.html')


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.http import HttpResponse
def chat_login(request):
    
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        print('aaaaaaaaaaaaaaaaaaaaaaaa', user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('lgon koebar korben')
    else:

        return render(request, 'auth/login.html')

