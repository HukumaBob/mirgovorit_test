from django.urls import path
from .views import (
    add_ingredient_to_recipe,
    cook_recipe,
    show_recipes_without_ingredient
    )

app_name = "cook_book"


urlpatterns = [
    path(
        'add_ingredient_to_recipe/',
        add_ingredient_to_recipe,
        name='add_ingredient_to_recipe'
        ),
    path(
        'cook_recipe/',
        cook_recipe, name='cook_recipe'
         ),
    path(
        'recipes_without_ingredient/',
        show_recipes_without_ingredient,
        name='recipes_without_ingredient'
        ),
]
