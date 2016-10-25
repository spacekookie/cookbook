
# Django requirements
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

# App specific django code
from .models import Recipe, Dish, DishCollection, Cook
from .forms import UserForm, LoginForm

# External requirements
from datetime import datetime as dt
import json


def index(request):
  current_user = request.user
  collections = DishCollection.objects.all()
  no_users = len(Cook.objects.all())

  return render(request, 'core/index.html', 
    { 
      'logged_in': request.user.is_authenticated(),
      'current_user': current_user,
      'collections': collections,
      'users': no_users
    })


def dish(request, id):
  current_user = request.user
  dish = get_object_or_404(Dish, pk=id)

  implementations = dish.recipies.all()
  print(implementations)

  return render(request, 'core/data_views/dish.html', 
    { 
      'logged_in': request.user.is_authenticated(),
      'current_user': current_user,
      'dish': dish,
      'recipies': implementations
    })


def collection(request, id):
  current_user = request.user
  collection = get_object_or_404(DishCollection, pk=id)

  dishes = collection.dishes.all()
  print(dishes)

  return render(request, 'core/data_views/collection.html', 
    { 
      'collection': collection,
      'dishes': dishes
    }
  )


def recipe(request, id):
  current_user = request.user
  recipe = get_object_or_404(Recipe, pk=id)

  instructions = json.loads(recipe.instructions)
  ingredients = recipe.ingredients.all()

  return render(request, 'core/data_views/recipe.html', 
    { 
      'recipe': recipe, 
      'instructions': instructions, 
      'ingredients': ingredients
    })


def register(request):
  current_user = request.user
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
    return render(request, template, 
      { 
        'logged_in': request.user.is_authenticated(),
        'current_user': current_user,
        'error_message': error, 'form': form
      })

  else:
    return render(request, template, 
      { 
        'logged_in': request.user.is_authenticated(),
        'current_user': current_user,
        'form': UserForm()
      })


def register_confirm(request, id):
  current_user = request.user
  username = None
  
  try:
    user = User.objects.get(pk=id)
    username = user.username

  except Exception as e:
    print(e)

  # Return a view for a newly registered user (or not)
  return render(request, 'core/register/confirm.html', 
    { 
      'logged_in': request.user.is_authenticated(),
      'current_user': current_user,
      'user_id': id, 'username': username
    })


def login(request):
  current_user = request.user
  template = 'core/login.html'

  if request.method == 'POST':
    form = LoginForm(request.POST)

    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']

      user = authenticate(username=username, password=password)

      if user is not None:
        django_login(request, user=user)
        print("Authentication successful!")

        return redirect(reverse('core:index'))
        
      else:
        print("Authentication FAILED!")
        return render(request, template, 
          { 
            'logged_in': request.user.is_authenticated(),
            'error_message': 'Authentication failed! User/ PW combination not known',
            'current_user': current_user,
            'form': LoginForm()
          })

  else:
    return render(request, template, 
      { 
        'logged_in': request.user.is_authenticated(),
        'current_user': current_user,
        'form': LoginForm()
      })


def profile(request, id):
  current_user = request.user

  user = get_object_or_404(User, pk=id)
  recipies = []

  try:
    recipies = Recipe.objects.filter(creator=user.cook)

  except Exception as e:
    print("Apparently an error occured")

  print(recipies)

  return render(request, 'core/internal/profile.html', 
    { 
      'logged_in': request.user.is_authenticated(),
      'current_user': current_user,
      'user': user,
      'recipies': recipies
   })


def profile_edit(request, id):
  current_user = request.user
  user = get_object_or_404(User, pk=id)
  error = None

  if user is not current_user:
    error = "Unable to edit user that is not self!"

  return render(request, 'core/internal/profile.html', 
    {
      'error': error,
      'logged_in': request.user.is_authenticated(),
      'current_user': current_user,
      'user': user
   })


def logout(request):
  current_user = request.user
  if current_user.username is not None:
    django_logout(request)
    return redirect(reverse('core:index'))


def list_view_users(request):
  current_user = request.user
  users = Cook.objects.all()

  print("Getting all users registered")
  
  return render(request, 'core/lists/users.html', 
    { 
      'logged_in': request.user.is_authenticated(),
      'current_user': current_user,
      'users': users,
      'number_users': len(users)
   })


def list_view_ingredients(request):
  current_user = request.user
  ingr = Ingredient.objects.all()
  
  return render(request, 'core/lists/ingredients.html', 
    { 
      'logged_in': request.user.is_authenticated(),
      'current_user': current_user,
      'user': user,
      'recipies': recipies
   })


def list_view_dishes(request):
  meals = Meal.objects.all()
  
  return render(request, 'core/lists/meals.html', 
    { 
      'logged_in': request.user.is_authenticated(),
      'current_user': current_user,
      'user': user,
      'recipies': recipies
   })