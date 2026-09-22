import json

from django.utils import timezone
from recipe_scrapers import scrape_html
from selenium import webdriver

from .models import Keyword, NutritionalInfo, Recipe


# Backup scraper for sites that require JavaScript to load
def backup_scraper(url):
    driver = webdriver.Firefox()
    driver.get(url)
    page = driver.page_source
    driver.quit()
    return page

# Takes a URL and HTML for a page containing a recipe schema
# Generates Recipe, Keyword, and Nutrition objects and saves them to the database
def add_recipe(url, html):
    scraper = scrape_html(html, org_url=url, supported_only=False)
    recipe = scraper.to_json()

    prepTime = None
    if recipe.get("prep_time") is not None:
        prepTime = timezone.timedelta(minutes=scraper.prep_time())
    totalTime = None
    if recipe.get("total_time") is not None:
        totalTime = timezone.timedelta(minutes=scraper.total_time())
    cookTime = None
    if recipe.get("cook_time") is not None:
        cookTime = timezone.timedelta(minutes=scraper.cook_time())

    r = Recipe(
        webAddress = recipe.get("canonical_url"),
        name = recipe.get("title"),
        author = recipe.get("author", "Unknown"),
        description = recipe.get("description"),
        image = recipe.get("image"),
        publisher = recipe.get("site_name"),
        prepTime = prepTime,
        totalTime = totalTime,
        cookTime = cookTime,
        cookingMethod = recipe.get("cooking_method"),
        recipeCategory = recipe.get("category"),
        recipeCuisine = recipe.get("cuisine"),
        recipeIngredient = json.dumps(scraper.ingredients()),
        recipeInstructions = json.dumps(scraper.instructions_list()),
        suitableForDiet = json.dumps(
            recipe.get("dietary_restrictions", [])
        ),
        dateSaved = timezone.now()
    )
    r.save()

    keywords = recipe.get("keywords")
    if keywords is not None:
        for word in keywords:
            k = Keyword(
                recipe = r,
                keyword = word.lower()
            )
            k.save()

    nutrients = recipe.get("nutrients")
    print(nutrients)
    if nutrients is not None and len(nutrients) > 0:
        n = NutritionalInfo(
            recipe = r,
            calories = nutrients.get("calories"),
            carbohydrateContent = nutrients.get("carbohydrateContent"),
            cholesterolContent = nutrients.get("cholesterolContent"),
            fatContent = nutrients.get("fatContent"),
            fiberContent = nutrients.get("fiberContent"),
            proteinContent = nutrients.get("proteinContent"),
            saturatedFatContent = nutrients.get("saturatedFatContent"),
            servingSize = nutrients.get("servingSize"),
            sodiumContent = nutrients.get("sodiumContent"),
            sugarContent = nutrients.get("sugarContent"),
            transFatContent = nutrients.get("transFatContent"),
            unsaturatedFatContent = nutrients.get("unsaturatedFatContent")
        )
        n.save()
