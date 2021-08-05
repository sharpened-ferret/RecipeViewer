from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from datetime import date
from dateutil.parser import *

from scrape_schema_recipe import scrape_url

from .models import Recipe
from .forms import AddRecipeForm

def index(request):
    return HttpResponse("Hello world")

def recipe(request):
    context = {}
    return render(request, 'viewer/index.html', context)

def addRecipe(request):
    

    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        
        if form.is_valid():
            url = form.cleaned_data['url']
            print("URL Recieved: " + url)

            recipe_list = scrape_url(url, python_objects=True)

            # Warning: The following code has a painful number of if/else statements. I kinda hate it tbh.
            # Unfortunately different sites have a habit of leaving out different schema sections. 
            # Hopefully I'll think of a better way of doing this in the future.
            if len(recipe_list) > 0:
                recipe = recipe_list[0]
                
                 # From Thing schema
                webAddress = recipe['url']
                name = recipe['name']
                description = recipe['description']

                if 'url' in recipe['image']:
                    image = recipe['image']['url']
                else:
                    image = recipe['image'][0]
                
                 # From Creative Work schema
                author = recipe['author']
                datePublished = parse(recipe['datePublished'])
                print(datePublished)
                if 'publisher' in recipe:
                    publisher = recipe['publisher']
                else:
                    publisher = None

                 # From How To schema
                if 'estimatedCost' in recipe:
                    estimatedCost = recipe['estimatedCost']
                else:
                    estimatedCost = None
                if 'prepTime' in recipe:
                    prepTime = recipe['prepTime']
                else:
                    prepTime = None
                if 'totalTime' in recipe:
                    totalTime = recipe['totalTime']
                else:
                    totalTime = None

                 # From Recipe schema
                if 'cookTime' in recipe:
                    cookTime = recipe['cookTime']
                else:
                    cookTime = None
                if 'cookingMethod' in recipe:
                    cookingMethod = recipe['cookingMethod']
                else:
                    cookingMethod = None
                if 'nutrition' in recipe:
                    nutrition = recipe['nutrition']
                else:
                    nutrition = None
                if 'recipeCategory' in recipe:
                    recipeCategory = recipe['recipeCategory']
                else:
                    recipeCategory = None
                if 'recipeCuisine' in recipe:
                    recipeCuisine = recipe['recipeCuisine']
                else:
                    recipeCuisine = None
                recipeIngredient = recipe['recipeIngredient']
                recipeInstructions = recipe['recipeInstructions']
                if 'suitableForDiet' in recipe:
                    suitableForDiet = recipe['suitableForDiet']
                else:
                    suitableForDiet = None

                dateSaved = timezone.now()

            
                r = Recipe(
                    webAddress = webAddress,
                    name = name,
                    description = description,
                    image = image,
                    author = author,
                    datePublished = datePublished,
                    publisher = publisher,
                    estimatedCost = estimatedCost,
                    prepTime = prepTime,
                    totalTime = totalTime,
                    cookTime = cookTime,
                    cookingMethod = cookingMethod,
                    #nutrition = nutrition,
                    recipeCategory = recipeCategory,
                    recipeCuisine = recipeCuisine,
                    recipeIngredient = recipeIngredient,
                    recipeInstructions = recipeInstructions,
                    suitableForDiet = suitableForDiet,
                    dateSaved = dateSaved
                )
                r.save()
            
                print("success?")

                if 'keywords' in recipe:
                    keywords = recipe['keywords']
                else:
                    keywords = None
                return HttpResponseRedirect('success')
            else:
                print("No recipes found")

            return HttpResponseRedirect('add-recipe-handler/')
    else:
        form = AddRecipeForm()
    return render(request, 'viewer/addRecipe.html', {'form' : form})

def failedAdd(request):
    context = {}
    return render(request, 'viewer/failedAdd.html', context)

def successAdd(request):
    context = {}
    return render(request, 'viewer/successAdd.html', context)