from django.db import models

class NutritionalInfo(models.Model):
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
class Recipe(models.Model):
    
     # From Thing schema
    webAddress = models.URLField()
    name = models.TextField()
    description = models.TextField()
    image = models.URLField()

     # From Creative Work schema
    author = models.TextField()
    datePublished = models.DateField()
    publisher = models.TextField()

     # From How To schema
    estimatedCost = models.DecimalField(max_digits = 5, decimal_places = 2)
    prepTime = models.DurationField()
    totalTime = models.DurationField()

     # From Recipe schema
    cookTime = models.DurationField()
    cookingMethod = models.TextField()
    nutrition = models.ForeignKey(NutritionalInfo, on_delete=models.CASCADE)
    recipeCategory = models.TextField()
    recipeCuisine = models.TextField()
    recipeIngredient = models.TextField() # may cause issues later, have to check
    recipeInstructions = models.TextField()
    suitableForDiet = models.TextField() # need to process enums for storage

    dateSaved = models.DateTimeField()

class Keyword(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    keyword = models.TextField()