from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/', views.recipe, name='recipe'),
    path('add-recipe/', views.addRecipe, name='add-recipe'),
]