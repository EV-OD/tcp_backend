from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import IP





def index(request):
   if request.user.is_authenticated:
       context = {'username': request.user.username}
       return render(request, "index.html", context)
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

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
      print("Someone tried to login.")
      return redirect('index')
  else:
    return render(request, 'login.html')
@csrf_protect
def registerUser(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            print(user)
            return redirect('index')
        except IntegrityError:
            print("User with this username already exists.")
            # Handle the case where the user with the provided username already exists
            # You might want to display an error message or redirect back to the registration form
            return render(request, 'registration_error.html')
        except Exception as e:
            print(f"Error creating user: {e}")
            return redirect('/')
    else:
        return render(request, 'index.html')
    
def logoutUser(request):
  logout(request)
  return redirect('index')

def reportPage(request):
  return render(request, 'reportPage.html')

def searchPage(request, ip):
  return render(request, 'search.html', {'ip': ip})

def autoflagPage(request):
    if request.method == "POST":
        ip = request.POST.get('ip')
        autoflag_ip = request.POST.get('autoflag_ip')
        existing_ip = IP.objects.filter(overall_ip=ip).first()
        if existing_ip:
            existing_ip.autoflag_count += 1
            existing_ip.set_autoflag_ip(existing_ip.get_autoflag_ip() + [autoflag_ip])
            existing_ip.save()
        else:
            new_ip = IP(overall_ip=ip, autoflag_count=1)
            new_ip.set_autoflag_ip([autoflag_ip])
            new_ip.save()

def setPublicFlag(request):
    if request.method == "POST":
        ip = request.POST.get('ip')
        publicflag_ip = request.POST.get('publicflag_ip')
        existing_ip = IP.objects.filter(overall_ip=ip).first()
        if existing_ip:
            existing_ip.publicflag_count += 1
            existing_ip.set_publicflag_ip(existing_ip.get_publicflag_ip() + [publicflag_ip])
            existing_ip.save()
        else:
            new_ip = IP(overall_ip=ip, publicflag_count=1)
            new_ip.set_publicflag_ip([publicflag_ip])
            new_ip.save()

def setAuthFlag(request):
    if request.method == "POST":
        ip = request.POST.get('ip')
        user = request.POST.get('user')
        existing_ip = IP.objects.filter(overall_ip=ip).first()
        if existing_ip:
            existing_ip.authflag_count += 1
            existing_ip.set_authflag_accounts(existing_ip.get_authflag_accounts() + [user])
            existing_ip.save()
        else:
            new_ip = IP(overall_ip=ip, authflag_count=1)
            new_ip.set_authflag_accounts([user])
            new_ip.save()
   




