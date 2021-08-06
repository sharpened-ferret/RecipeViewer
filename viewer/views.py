from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from datetime import date
from dateutil.parser import *

from scrape_schema_recipe import scrape_url

from .models import Recipe, NutritionalInfo, Keyword
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
                if isinstance(recipe['author'], list):
                    if 'name' in recipe['author'][0]:
                        author = recipe['author'][0]['name']
                    
                    else:
                        author = recipe['author'][0]
                else:
                    if isinstance(recipe['author'], str):
                        author = recipe['author']
                    elif 'name' in recipe['author']:
                        author = recipe['author']['name']
                    else:
                        author = 'UNKNOWN'
                if 'datePublished' in recipe:
                    if isinstance(recipe['datePublished'], str):
                        datePublished = parse(recipe['datePublished'])
                    elif isinstance(recipe['datePublished'], date):
                        datePublished = recipe['datePublished']
                    else:
                        datePublished = recipe['datePublished'].date()
                else:
                    datePublished = None
                if 'publisher' in recipe:
                    if 'name' in recipe['publisher']:
                        publisher = recipe['publisher']['name']
                    else:
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
                if isinstance(recipe['recipeInstructions'], list):
                    if '@type' in recipe['recipeInstructions'][0]:
                        outputText = "<ol>"
                        for x in range(0, len(recipe['recipeInstructions'])):
                            currentStep = x
                            outputText += "<li>" + recipe['recipeInstructions'][x]['text'] + "</li>"
                        outputText += "</ol>"
                        recipeInstructions = outputText
                    elif len(recipe['recipeInstructions']) > 1:
                        outputText = "<ol>"
                        for howToStep in recipe['recipeInstructions']:
                            outputText += "<li>" + recipe['recipeInstructions'][howToStep]['text'] + "</li>"
                        outputText += "</ol>"
                        recipeInstructions = outputText
                    else:
                        recipeInstructions = "<p>" + recipe['recipeInstructions'][0] + "</p>"
                else:
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
                    recipeCategory = recipeCategory,
                    recipeCuisine = recipeCuisine,
                    recipeIngredient = recipeIngredient,
                    recipeInstructions = recipeInstructions,
                    suitableForDiet = suitableForDiet,
                    dateSaved = dateSaved
                )
                r.save()


                # Keywords Handling
                if 'keywords' in recipe:
                    keywords = []
                    if isinstance(recipe['keywords'], str):
                        keywords = recipe['keywords'].split(", ")
                    elif isinstance(recipe['keywords'], list):
                        keywords = recipe['keywords']
                    print(recipe['keywords'])
                    print(keywords)
                    if len(keywords) > 0:
                        for word in keywords:
                            k = Keyword(
                                    recipe = r, 
                                    keyword = word
                                )
                            k.save()
                    


                # Nutritional Info Handling (Where exists)
                if 'nutrition' in recipe:
                    if 'calories' in recipe['nutrition']:
                        calories = recipe['nutrition']['calories']
                    else:
                        calories = None
                    if 'carbohydrateContent' in recipe['nutrition']:
                        carbohydrateContent = recipe['nutrition']['carbohydrateContent']
                    else:
                        carbohydrateContent = None
                    if 'cholesterolContent' in recipe['nutrition']:
                        cholesterolContent = recipe['nutrition']['cholesterolContent']
                    else:
                        cholesterolContent = None
                    if 'fatContent' in recipe['nutrition']:
                        fatContent = recipe['nutrition']['fatContent']
                    else:
                        fatContent = None
                    if 'fiberContent' in recipe['nutrition']:
                        fiberContent = recipe['nutrition']['fiberContent']
                    else:
                        fiberContent = None
                    if 'proteinContent' in recipe['nutrition']:
                        proteinContent = recipe['nutrition']['proteinContent']
                    else:
                        proteinContent = None
                    if 'saturatedFatContent' in recipe['nutrition']:
                        saturatedFatContent = recipe['nutrition']['saturatedFatContent']
                    else:
                        saturatedFatContent = None
                    if 'servingSize' in recipe['nutrition']:
                        servingSize = recipe['nutrition']['servingSize']
                    else:
                        servingSize = None
                    if 'sodiumContent' in recipe['nutrition']:
                        sodiumContent = recipe['nutrition']['sodiumContent']
                    else:
                        sodiumContent = None
                    if 'sugarContent' in recipe['nutrition']:
                        sugarContent = recipe['nutrition']['sugarContent']
                    else:
                        sugarContent = None
                    if 'transFatContent' in recipe['nutrition']:
                        transFatContent = recipe['nutrition']['transFatContent']
                    else:
                        transFatContent = None
                    if 'unsaturatedFatContent' in recipe['nutrition']:
                        unsaturatedFatContent = recipe['nutrition']['unsaturatedFatContent']
                    else:
                        unsaturatedFatContent = None
                    
                    
                    n = NutritionalInfo(
                        calories = calories,
                        carbohydrateContent = carbohydrateContent,
                        cholesterolContent = cholesterolContent,
                        fatContent = fatContent,
                        fiberContent = fiberContent,
                        proteinContent = proteinContent,
                        saturatedFatContent = saturatedFatContent,
                        servingSize = servingSize,
                        sodiumContent = sodiumContent,
                        sugarContent = sugarContent,
                        transFatContent = transFatContent,
                        unsaturatedFatContent = unsaturatedFatContent,
                        recipe = r
                    )
                    n.save()
                    print("Success")
                return HttpResponseRedirect('success')
            else:
                print("No compatible recipes found")

            return HttpResponseRedirect('failed')
    else:
        form = AddRecipeForm()
    return render(request, 'viewer/addRecipe.html', {'form' : form})

def failedAdd(request):
    context = {}
    return render(request, 'viewer/failedAdd.html', context)

def successAdd(request):
    context = {}
    return render(request, 'viewer/successAdd.html', context)