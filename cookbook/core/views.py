from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from django.contrib.auth.models import User
from .models import Recipe, Dish, DishCollection, Cook
from .forms import UserForm

import json

def index(request):
  collections = DishCollection.objects.all()
  no_users = len(Cook.objects.all())

  return render(request, 'core/index.html', { 'collections': collections, 'users': no_users })


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


def register(request):
  if request.method == 'POST':
    print(request.POST)

    form = UserForm(request.POST)
    if form.is_valid():
      print(form.cleaned_data)

      user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
      cook = Cook.objects.create(user=user)

      return render(request, 'core/register.html', { 'error_message': 'SUCCESS!', 'form': UserForm() })

    else:
      return render(request, 'core/register.html', { 'error_message': 'Form is invalid!' })
  else:
    return render(request, 'core/register.html', { 'form': UserForm() })


def login(request):
  pass