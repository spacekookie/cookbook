from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Recipe, Dish, DishCollection

import json

def index(request):
    return HttpResponse("This is where the cookbook index will one day be!")


def dish(request, id):
  dish = get_object_or_404(Dish, pk=id)

  implementations = dish.recipies.all()
  print(implementations)

  return render(request, 'core/dish.html', { 'dish': dish, 'recipies': implementations })


def collection(request, id):
  collection = get_object_or_404(DishCollection, pk=id)

  dishes = collection.dishes.all()
  print(dishes)

  return render(request, 'core/collection.html', 
    { 
      'collection': collection,
      'dishes': dishes
    }
  )


def recipe(request, id):
  recipe = get_object_or_404(Recipe, pk=id)

  instructions = json.loads(recipe.instructions)
  ingredients = recipe.ingredients.all()

  return render(request, 'core/recipe.html', 
    { 
      'recipe': recipe, 
      'instructions': instructions, 
      'ingredients': ingredients
    })
