from django.contrib import admin
from .models import Cook, Category, DishCollection, Dish, Ingredient, Recipe, Picture


admin.site.register(Picture)
admin.site.register(Cook)
admin.site.register(Category)
admin.site.register(DishCollection)
admin.site.register(Dish)
admin.site.register(Ingredient)
admin.site.register(Recipe)
