from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    times_cooked = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
        )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
        )
    weight = models.IntegerField(default=0)

    def __str__(self):
        return (f'{self.recipe.name} '
                f'({self.ingredient.name}, '
                f'вес: {self.weight})')
