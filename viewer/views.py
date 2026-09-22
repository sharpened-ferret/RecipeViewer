import json

import requests
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from recipe_scrapers import NoSchemaFoundInWildMode

from viewer.utils import add_recipe, backup_scraper

from .forms import AddRecipeForm, SearchForm
from .models import AddRecipeManual, Keyword, NutritionalInfo, Recipe


# App homepage
def index(request):
    context = {}
    return render(request, 'viewer/index.html', context)

# Displays a stored recipe to the user
# Takes an integer recipe ID to select which recipe to display
def recipe(request, recipe_id):
    recipe = Recipe.objects.filter(id = recipe_id).first()

    if recipe.estimatedCost == None:
        estimatedCost = "Unknown"
    else:
        estimatedCost = recipe.estimatedCost

    ingredients_list = "<ul id='ingredients-list'>"
    for ingredient in json.loads(recipe.recipeIngredient):
        ingredients_list += "<li>" + ingredient + "</li>"
    ingredients_list += "</ul>"

    if recipe.cookTime == None:
        cookTime = "Unspecified"
    else:
        cookTime = recipe.cookTime
    if recipe.prepTime == None:
        prepTime = "Unspecified"
    else:
        prepTime = recipe.prepTime
    if recipe.totalTime == None:
        totalTime = "Unspecified"
    else:
        totalTime = recipe.totalTime

    diet_type = json.loads(recipe.suitableForDiet)
    instructions = "<ol id='instructions-list'>"
    for step in json.loads(recipe.recipeInstructions):
        instructions += "<li>" + step + "</li>"
    instructions += "</ol>"

    context = {
        'name' : recipe.name,
        'image_url' : recipe.image,
        'description' : recipe.description,
        'ingredients_list' : ingredients_list,
        'instructions_list' : instructions,
        'recipe_category' : recipe.recipeCategory,
        'recipe_cuisine' : recipe.recipeCuisine,
        'diet_type' : ' '.join(diet_type),
        'estimated_cost' : estimatedCost,
        'author' : recipe.author,
        'publisher' : recipe.publisher,
        'date_published' : recipe.datePublished,
        'cook_time' : cookTime,
        'prep_time' : prepTime,
        'total_time' : totalTime,

        'date_saved' : recipe.dateSaved.strftime("%A %d %B %Y %X"),
        'url' : recipe.webAddress
    }

    if NutritionalInfo.objects.filter(recipe_id = recipe_id).count() > 0:
        nutritionalInfo = NutritionalInfo.objects.filter(recipe_id = recipe_id).first()

        context['calories'] = nutritionalInfo.calories
        context['carbohydrates'] = nutritionalInfo.carbohydrateContent
        context['sugar'] = nutritionalInfo.sugarContent
        context['cholesterol'] = nutritionalInfo.cholesterolContent
        context['fat'] = nutritionalInfo.fatContent
        context['fat_saturated'] = nutritionalInfo.saturatedFatContent
        context['fat_unsaturated'] = nutritionalInfo.unsaturatedFatContent
        context['fat_trans'] = nutritionalInfo.transFatContent
        context['fibre'] = nutritionalInfo.fiberContent
        context['protein'] = nutritionalInfo.proteinContent
        context['sodium'] = nutritionalInfo.sodiumContent
        context['serving_size'] = nutritionalInfo.servingSize

        return render(request, 'viewer/viewRecipeNutrition.html', context)
    else:
        return render(request, 'viewer/viewRecipe.html', context)

# Allows users to add recipes via a URL to a page containing a recipe Schema or HTML recipes from compatible websites
# Compatibility list is available at https://docs.recipe-scrapers.com/getting-started/supported-sites/
def addRecipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            print("URL Recieved: " + url)

            # TODO: Configure when to use request vs browser to fetch recipes
            response = requests.get(url)
            html = response.text
            # html = backup_scraper(url)
            if response.status_code == 403:
                html = backup_scraper(url)

            try:
                add_recipe(url, html)
                return HttpResponseRedirect('success')
            # Fallback for if the page contains no valid schema
            except NoSchemaFoundInWildMode:
                print("No compatible recipes found")
                return HttpResponseRedirect('failed')
    else:
        form = AddRecipeForm()
    return render(request, 'viewer/addRecipe.html', {'form' : form})

# WIP
# Allows users to manually submit recipes by entering the relevant form data
def addRecipeManual(request):
    if request.method == "POST":
        print(request.POST)
        form = AddRecipeManual(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('success')
    else:
        form = AddRecipeManual()
        context = {
            'manual_recipe_form' : form
        }
        return render(request, 'viewer/addRecipeManual.html', context)

# Served when a submitted recipe fails to upload to the database.
# Usually this is when no valid recipe schema could be found on the page.
def failedAdd(request):
    context = {}
    return render(request, 'viewer/failedAdd.html', context)

# Displayed on successful submission of a new recipe
def successAdd(request):
    context = {}
    return render(request, 'viewer/successAdd.html', context)

# Search page for stored recipes
def search(request):
    if request.method == 'POST':
        searchForm = SearchForm(request.POST)

        if searchForm.is_valid():
            searchTerm = searchForm.cleaned_data['searchTerm']
            print("Search Term Recieved: " + searchTerm)


            results = ""
            resultFormat = '<div class="search-result"><a href="./recipe/{id}"><div class="clickable-area"><h2>{name}</h2><p>{description}</p><img src="{image}" alt="Recipe Image"></div></a></div>'

            # Stores IDs of returned recipes to prevent returning any multiple times
            existingResults = []

            # "*" Search command to return all results
            if searchTerm == "*":
                allRecipes = Recipe.objects.all()
                for recipe in allRecipes:
                    results += resultFormat.format(
                            id = recipe.id,
                            name = recipe.name,
                            description = recipe.description,
                            image = recipe.image
                        )
                    existingResults.append(recipe.id)
            else:
                # Searches recipe names and keywords  -  fairly primitive
                # This could probably be improved by migrating to a DBMS with more advanced text search (eg. PostGreSQL)
                exactMatch = Recipe.objects.filter(name__iexact = searchTerm)
                titleMatch = Recipe.objects.filter(name__icontains = searchTerm)
                keywordMatch = Keyword.objects.filter(keyword__icontains = searchTerm).values('recipe')
                # Returns exact matches first, followed by partial title matches, and finally keyword tags
                for recipe in exactMatch:
                    if recipe.id not in existingResults:
                        results += resultFormat.format(
                            id = recipe.id,
                            name = recipe.name,
                            description = recipe.description,
                            image = recipe.image
                        )

                        existingResults.append(recipe.id)
                for recipe in titleMatch:
                    if recipe.id not in existingResults:
                        results += resultFormat.format(
                            id = recipe.id,
                            name = recipe.name,
                            description = recipe.description,
                            image = recipe.image
                        )
                        existingResults.append(recipe.id)
                for keyword in keywordMatch:
                    recipe_id = keyword['recipe']
                    if recipe_id not in existingResults:
                        recipe = Recipe.objects.filter(id = recipe_id).first()
                        results += resultFormat.format(
                            id = recipe.id,
                            name = recipe.name,
                            description = recipe.description,
                            image = recipe.image
                        )
                        existingResults.append(recipe_id)

            if len(existingResults) == 0:
                results = "<h2>No recipes found.</h2>"

            return render(request, 'viewer/searchResults.html', {'searchForm' : searchForm, 'search_results' : results})


        else:
            searchForm = SearchForm()
    else:
        searchForm = SearchForm()

    return render(request, 'viewer/search.html', {'searchForm' : searchForm})

# Serves a Json file, containing all recipes, nutritional data, and keywords in the database
# Intended for backups / major version switches / export to other applications
def export(request):
    recipes = Recipe.objects.all()
    nutritions = NutritionalInfo.objects.all()
    keywords = Keyword.objects.all()

    json_return = {
        'Data_version' : 'alpha-0.01',
        'Recipes' : serialize("json", recipes),
        'Nutritions' : serialize("json", nutritions),
        'Keywords' : serialize("json", keywords)
    }
    return JsonResponse(json_return)
