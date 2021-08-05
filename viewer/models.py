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
    image = models.URLField(blank=True, null=True)

     # From Creative Work schema
    author = models.TextField()
    datePublished = models.DateField()
    publisher = models.TextField(blank=True, null=True)

     # From How To schema
    estimatedCost = models.DecimalField(max_digits = 5, decimal_places = 2, blank=True, null=True)
    prepTime = models.DurationField(blank=True, null=True)
    totalTime = models.DurationField(blank=True, null=True)

     # From Recipe schema
    cookTime = models.DurationField(blank=True, null=True)
    cookingMethod = models.TextField(blank=True, null=True)
    nutrition = models.ForeignKey(NutritionalInfo, on_delete=models.CASCADE, blank=True, null=True)
    recipeCategory = models.TextField(blank=True, null=True)
    recipeCuisine = models.TextField(blank=True, null=True)
    recipeIngredient = models.TextField() # may cause issues later, have to check
    recipeInstructions = models.TextField()
    suitableForDiet = models.TextField(blank=True, null=True) # need to process enums for storage

    dateSaved = models.DateTimeField()

class Keyword(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    keyword = models.TextField()