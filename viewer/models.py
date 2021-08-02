from django.db import models

class Keyword(models.model):
    recipe = models.ForeignKey()
    keyword = models.TextField()

class NutritionalInfo(models.model):
    calories = models.TextField()
    carbohydrateContent = models.TextField()
    cholesterolContent = models.TextField()
    fatContent = models.TextField()
    fiberContent = models.TextField()
    proteinContent = models.TextField()
    saturatedFatContent = models.TextField()
    servingSize = models.TextField()
    sodiumContent = models.TextField()
    sugarContent = models.TextField()
    transFatContent = models.TextField()
    unsaturatedFatContent = models.TextField()

# Create your models here.
class Recipe(models.model):
    
    webAddress = models.URLField()
    name = models.TextField()
    description = models.TextField()
    image = models.models.URLField()

    author = models.TextField()
    datePublished = models.models.DateField()
    publisher = models.TextField()

    estimatedCost = models.DecimalField()
    prepTime = models.DurationField()
    totalTime = models.DurationField()

    cookTime = models.DurationField()
    cookingMethod = models.TextField()
    nutrition = models.ForeignKey(NutritionalInfo)
    recipeCategory = models.TextField()
    recipeCuisine = models.TextField()
    recipeIngredient = models.TextField() # may cause issues later, have to check
    recipeInstructions = models.TextField()
    suitableForDiet = models.TextField() # need to process enums for storage

    # keywords = models.ForeignKey() probably not needed