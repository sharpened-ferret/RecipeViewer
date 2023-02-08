from django.db import models
from django.forms import ModelForm

# Defines a recipe data model
# based on https://schema.org/Recipe
class Recipe(models.Model):
    def __str__(self):
        return self.name
    
     # From Thing schema
     # https://schema.org/Thing
    webAddress = models.URLField()
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

     # From Creative Work schema
     # https://schema.org/CreativeWork
    author = models.TextField()
    datePublished = models.DateField(blank=True, null=True)
    publisher = models.TextField(blank=True, null=True)

     # From How To schema
     # https://schema.org/HowTo
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

    # Non-schema - added for app functionality
    dateSaved = models.DateTimeField()

# Form for manual entry of Recipe data
class AddRecipeManual(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        

# Describes a recipe's nutritional information
# based on https://schema.org/NutritionInformation
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

# Keywords map keyword -> Recipe
# Used to improve recipe searching
class Keyword(models.Model):
    def __str__(self):
        return self.keyword + " | " + self.recipe.name

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    keyword = models.TextField()