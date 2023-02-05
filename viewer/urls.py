from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>', views.recipe, name='recipe'),
    path('add-recipe/', views.addRecipe, name='add-recipe'),
    path('add-recipe-manual/', views.addRecipeManual, name='add-recipe'),
    path('add-recipe/failed', views.failedAdd, name='add-recipe-failed'),
    path('add-recipe/success', views.successAdd, name='add-recipe-success'),
    path('search', views.search, name='search'),
]