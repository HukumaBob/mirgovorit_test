from django.http import JsonResponse, Http404
from django.shortcuts import render
from .models import Ingredient, Recipe, RecipeIngredient


def add_ingredient_to_recipe(request):
    """
    Add an ingredient to a recipe or update the weight of the
    ingredient in the recipe.

    Parameters:
    request (HttpRequest): The HTTP request from the client. 
    It should contain 'recipe_id', 'ingredient_id', 
    and 'weight' as GET parameters.

    Returns:
    JsonResponse: A JSON response indicating whether 
    the operation was successful.
    """
    try:
        recipe_id = request.GET.get('recipe_id')
        ingredient_id = request.GET.get('ingredient_id')
        weight = request.GET.get('weight')

        recipe = Recipe.objects.get(id=recipe_id)
        ingredient = Ingredient.objects.get(id=ingredient_id)

        recipe_ingredient, created = RecipeIngredient.objects.get_or_create(
            recipe=recipe, ingredient=ingredient, defaults={'weight': weight}
        )

        if weight is not None:
            recipe_ingredient.weight += int(weight)
            recipe_ingredient.save()

        return JsonResponse(
            {
                'success': True,
                'recipe': {
                    'id': recipe.id,
                    'name': recipe.name,
                    },
                'ingredient': {
                    'id': ingredient.id,
                    'name': ingredient.name,
                },
                'total weight': recipe_ingredient.weight,
                }
                )
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")
    except Ingredient.DoesNotExist:
        raise Http404("Ingredient does not exist")


def cook_recipe(request):
    """
    Cook a recipe. This increases the 'times_cooked' 
    field of each ingredient in the recipe by 1.

    Parameters:
    request (HttpRequest): The HTTP request from the client. 
    It should contain 'recipe_id' as a GET parameter.

    Returns:
    JsonResponse: A JSON response indicating whether the 
    operation was successful.
    """
    try:
        recipe_id = request.GET.get('recipe_id')
        recipe = Recipe.objects.get(id=recipe_id)

        for recipe_ingredient in recipe.recipeingredient_set.all():
            recipe_ingredient.ingredient.times_cooked += 1
            recipe_ingredient.ingredient.save()

        return JsonResponse(
            {
                'success': True,
                'times cooked': recipe_ingredient.ingredient.times_cooked
                }
                )
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")


def show_recipes_without_ingredient(request):
    """
    Show recipes that do not contain a specific 
    ingredient or contain it in a quantity less than 10 grams.

    Parameters:
    request (HttpRequest): The HTTP request from the client. 
    It should contain 'ingredient_id' as a GET parameter.

    Returns:
    HttpResponse: An HTML page showing the recipes without 
    the specified ingredient.
    """
    try:
        ingredient_id = request.GET.get('ingredient_id')
        ingredient = Ingredient.objects.get(id=ingredient_id)

        recipes = (
            Recipe.objects.exclude(
                recipeingredient__ingredient=ingredient
                ) | Recipe.objects.filter(
                    recipeingredient__ingredient=ingredient,
                    recipeingredient__weight__lt=10
                    )
            ).distinct()

        context = {
            'recipes': recipes,
        }

        return render(
            request, 'recipes/recipes_without_ingredient.html',
            context
            )
    except Ingredient.DoesNotExist:
        raise Http404("Ingredient does not exist")
