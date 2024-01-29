from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3

class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'times_cooked')

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
