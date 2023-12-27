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
import json
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from .utils import hash_string







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
  flag = getFlagWithIp(ip)
  if(flag):
    return render(request, 'search.html', {'ip': ip, 'flag': flag})
  else:
    return render(request, 'search.html', {'ip': ip, 'flag': 0})
  

@csrf_exempt
def autoflagPage(request):
    if request.method == "POST":
        request_data = json.loads(request.body.decode('utf-8'))

        autoflag_ip = request_data.get('autoflag_ip')
        ip = request_data.get('ip')

        hashed_ip = hash_string(ip)
        existing_ip = IP.objects.filter(overall_ip=hashed_ip).first()
        if existing_ip:
            existing_ip.autoflag_count += 1
            existing_ip.set_autoflag_ip(existing_ip.get_autoflag_ip() + [autoflag_ip])
            existing_ip.save()
        else:
            new_ip = IP(overall_ip=ip, autoflag_count=1)
            new_ip.set_autoflag_ip([autoflag_ip])
            new_ip.save()
        return HttpResponse(status=200)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def setPublicFlag(request):
    if request.method == "POST":
        try:
            request_data = json.loads(request.body.decode('utf-8'))

            ip = request_data.get('ip')
            publicflag_ip = get_client_ip(request)  # Make sure to define or import get_client_ip
            hashed_ip = hash_string(ip)  # Hash the IP before querying the database

            existing_ip = IP.objects.filter(overall_ip=hashed_ip).first()

            if existing_ip:
                # Update existing IP entry
                existing_ip.publicflag_count += 1
                existing_ip.set_publicflag_ip(existing_ip.get_publicflag_ip() + [publicflag_ip])
                existing_ip.save()
            else:
                # Create a new IP entry
                new_ip = IP(overall_ip=hashed_ip, publicflag_count=1)
                new_ip.set_publicflag_ip([publicflag_ip])
                new_ip.save()

            return HttpResponse(status=200)

        except json.JSONDecodeError:
            return HttpResponse(status=400, content="Invalid JSON data")

    return HttpResponse(status=405)  # Method Not Allowed for non-POST requests

@csrf_exempt
def setAuthFlag(request):
    if request.method == "POST":
        try:
            request_data = json.loads(request.body.decode('utf-8'))

            user = request.user
            ip = request_data.get('ip')
            hashed_ip = hash_string(ip)  # Hash the IP before querying the database

            existing_ip = IP.objects.filter(overall_ip=hashed_ip).first()

            if existing_ip:
                # Update existing IP entry
                existing_ip.authflag_count += 1
                existing_ip.set_authflag_accounts(existing_ip.get_authflag_accounts() + [user])
                existing_ip.save()
            else:
                # Create a new IP entry
                new_ip = IP(overall_ip=hashed_ip, authflag_count=1)
                new_ip.set_authflag_accounts([user])
                new_ip.save()

            return HttpResponse(status=200)

        except json.JSONDecodeError:
            return HttpResponse(status=400, content="Invalid JSON data")

    return HttpResponse(status=405)  # Method Not Allowed for non-POST requests

@csrf_exempt
def getFlag(request):
    if request.method == "POST":
        try:
            request_data = json.loads(request.body.decode('utf-8'))

            ip = request_data.get('ip')
            hashed_ip = hash_string(ip)  # Hash the IP before querying the database

            existing_ip = IP.objects.filter(overall_ip=hashed_ip).first()
            if existing_ip:
                return HttpResponse(json.dumps(model_to_dict(existing_ip)))
            else:
                return HttpResponse("0")

        except json.JSONDecodeError:
            return HttpResponse(status=400, content="Invalid JSON data")

    return HttpResponse(status=405)  # Method Not Allowed for non-POST requests
        
@csrf_exempt
def checkIp(request):
    if request.method == "POST":
        request_data = json.loads(request.body.decode('utf-8'))

        ip = request_data.get('ip')
        existing_ip = IP.objects.filter(overall_ip=ip).first()
        if existing_ip:
            return HttpResponse("true")
        else:
            return HttpResponse("false")

def getFlagWithIp(ip):
    existing_ip = IP.objects.filter(overall_ip=hash_string(ip)).first()
    if existing_ip:
        return model_to_dict(existing_ip)
    else:
        return False
    


   




