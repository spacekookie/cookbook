
# Django requirements
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# App specific django code
from .models import Recipe, Dish, DishCollection, Cook
from .forms import UserForm, LoginForm

# External requirements
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
  template = 'core/register/register.html'
  error = 'Form data not valid!'

  if request.method == 'POST':

    print("Checking if the form is valid...")
    form = UserForm(request.POST)

    if form.is_valid():

      try:
        print("Creating user with username: %s" % form.cleaned_data['username'])
        user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])

        print("Creating new cook with attached FOOBAR!")
        cook = Cook.objects.create(user=user)

        # Redirect to a confirm page for the registration
        return HttpResponseRedirect(reverse('core:register_confirm', args=(user.id,)))

      except Exception as e:
        print(e.message)
        error = "User registration failed because: '%s'" % e.message

    print(form.errors)

    # In case we didn't return with a re-direct, we need to return an error message here
    return render(request, template, { 'error_message': error, 'form': form })

  else:
    return render(request, template, { 'form': UserForm() })


def register_confirm(request, id):
  username = None
  
  try:
    user = User.objects.get(pk=id)
    username = user.username

  except Exception as e:
    print(e)

  # Return a view for a newly registered user (or not)
  return render(request, 'core/register/confirm.html', { 'user_id': id, 'username': username })


def login(request):
  template = 'core/login.html'

  if request.method == 'POST':
    form = LoginForm(request.POST)

    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']

      user = authenticate(username=username, password=password)

      if user is not None:
        print("Authentication successful!")
        # A backend authenticated the credentials
        
      else:
        print("Authentication FAILED!")
        # No backend authenticated the credentials

      return render(request, template, { 'form': LoginForm() })

  else:
    return render(request, template, { 'form': LoginForm() })