from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render,redirect
from .models import tbl_authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



def index(request):
   return render(request, "index.html")

def loginPage(request):
  return render(request, 'login.html')

def registerPage(request):
  return render(request, 'register.html')



@csrf_protect
def loginUser(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
      user = tbl_authenticate.empAuth_objects.get(username = username, password = password)
      if user is not None:
         return redirect('index')
      else:
        print("someone tried to login.")

        return redirect('index')
    except Exception as identifier:
       return redirect('/')
  else:
    return render(request, 'index.html')
@csrf_protect
def registerUser(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
      user = tbl_authenticate.empAuth_objects.get(username = username, password = password)
      if user is not None:
         return redirect('index')
      else:
        print("someone tried to login.")

        return redirect('index')
    except Exception as identifier:
       return redirect('/')
  else:
    return render(request, 'index.html')
    
    

def reportPage(request):
  return render(request, 'reportPage.html')

def searchPage(request, ip):
  return render(request, 'search.html', {'ip': ip})





