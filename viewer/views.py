from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone

from scrape_schema_recipe import scrape_url

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
            url = form.cleaned_data['url']
            print("URL Recieved: " + url)

            recipe_list = scrape_url(url, python_objects=True)
            if len(recipe_list) > 0:
                recipe = recipe_list[0]
                
                 # From Thing schema
                webAddress = recipe['url']
                name = recipe['name']
                description = recipe['description']
                image = recipe['image']
                
                 # From Creative Work schema
                author = recipe['author']
                datePublished = recipe['datePublished']
                if 'publisher' in recipe:
                    publisher = recipe['publisher']
                else:
                    publisher = None

                 # From How To schema
                if 'estimatedCost' in recipe:
                    estimatedCost = recipe['estimatedCost']
                else:
                    estimatedCost = None
                prepTime = recipe['prepTime']
                totalTime = recipe['totalTime']

                 # From Recipe schema
                cookTime = recipe['cookTime']
                if 'cookingMethod' in recipe:
                    cookingMethod = recipe['cookingMethod']
                else:
                    cookingMethod = None
                nutrition = recipe['nutrition']
                recipeCategory = recipe['recipeCategory']
                recipeCuisine = recipe['recipeCuisine']
                recipeIngredient = recipe['recipeIngredient']
                recipeInstructions = recipe['recipeInstructions']
                if 'suitableForDiet' in recipe:
                    suitableForDiet = recipe['suitableForDiet']
                else:
                    suitableForDiet = None

                dateSaved = timezone.now()

                if 'keywords' in recipe:
                    keywords = recipe['keywords']
                else:
                    keywords = None
            else:
                print("No recipes found")

            return HttpResponseRedirect('add-recipe-handler/')
    else:
        form = AddRecipeForm()
    return render(request, 'viewer/addRecipe.html', {'form' : form})