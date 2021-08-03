from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Recipe

def index(request):
    return HttpResponse("Hello world")

def recipe(request):
    template = loader.get_template('viewer/index.html')
    context = {}
    return render(request, 'viewer/index.html', context)