from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Recipe

import json

def index(request):
    return HttpResponse("This is where the cookbook index will one day be!")


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
