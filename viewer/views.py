from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Recipe
from .forms import AddRecipeForm

def index(request):
    return HttpResponse("Hello world")

def recipe(request):
    template = loader.get_template('viewer/index.html')
    context = {}
    return render(request, 'viewer/index.html', context)

def addRecipe(request):
    template = loader.get_template('viewer/addRecipe.html')

    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        
        if form.is_valid():
            return HttpResponseRedirect('add-recipe-handler/')
    else:
        form = AddRecipeForm()
    return render(request, 'viewer/addRecipe.html', {'form' : form})