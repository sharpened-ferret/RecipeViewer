from django.db import models

# Create your models here.
class Recipe(models.Model):
    def __str__(self):
        return self.name + " recipe"
    
     # From Thing schema
    webAddress = models.URLField()
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

     # From Creative Work schema
    author = models.TextField()
    datePublished = models.DateField(blank=True, null=True)
    publisher = models.TextField(blank=True, null=True)

     # From How To schema
    estimatedCost = models.DecimalField(max_digits = 5, decimal_places = 2, blank=True, null=True)
    prepTime = models.DurationField(blank=True, null=True)
    totalTime = models.DurationField(blank=True, null=True)

     # From Recipe schema
    cookTime = models.DurationField(blank=True, null=True)
    cookingMethod = models.TextField(blank=True, null=True)
    recipeCategory = models.TextField(blank=True, null=True)
    recipeCuisine = models.TextField(blank=True, null=True)
    recipeIngredient = models.TextField() # may cause issues later, have to check
    recipeInstructions = models.TextField()
    suitableForDiet = models.TextField(blank=True, null=True) # need to process enums for storage

    dateSaved = models.DateTimeField()

class NutritionalInfo(models.Model):
    def __str__(self):
        return self.recipe.name + " nutritional info"

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    calories = models.TextField(blank=True, null=True)
    carbohydrateContent = models.TextField(blank=True, null=True)
    cholesterolContent = models.TextField(blank=True, null=True)
    fatContent = models.TextField(blank=True, null=True)
    fiberContent = models.TextField(blank=True, null=True)
    proteinContent = models.TextField(blank=True, null=True)
    saturatedFatContent = models.TextField(blank=True, null=True)
    servingSize = models.TextField(blank=True, null=True)
    sodiumContent = models.TextField(blank=True, null=True)
    sugarContent = models.TextField(blank=True, null=True)
    transFatContent = models.TextField(blank=True, null=True)
    unsaturatedFatContent = models.TextField(blank=True, null=True)


class Keyword(models.Model):
    def __str__(self):
        return self.keyword + " | " + self.recipe.name

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    keyword = models.TextField()