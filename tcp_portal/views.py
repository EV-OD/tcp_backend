from django.http import HttpResponse
from django.template import loader

def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

def loginPage(request):
  template = loader.get_template('login.html')
  return HttpResponse(template.render())

def registerPage(request):
  template = loader.get_template('register.html')
  return HttpResponse(template.render())
