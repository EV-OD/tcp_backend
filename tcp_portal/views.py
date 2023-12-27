from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render



def index(request):
   return render(request, "index.html")

def loginPage(request):
  return render(request, 'login.html')

def registerPage(request):
  return render(request, 'register.html')

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages

@csrf_protect
def loginUser(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')

    return redirect('index')
@csrf_protect
def registerUser(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    return redirect('index')




