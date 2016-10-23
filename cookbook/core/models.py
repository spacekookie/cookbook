import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Cook(models.Model):
  """ A wrapper around the Django user """
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  
  class Meta:
    verbose_name_plural = "Cooks"

  def __str__(self):
    return self.user.username


class Category(models.Model):
  """
  A category is a collection of meals that are similar. Acceptable categories would
  for example be:
    - Desert
    - Dinner
    - 

  A Dish can be part of multiple categories (e.g. Dinner & Vegetarian)
  """

  name = models.CharField(max_length=100)
  description = models.TextField()

  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = "Categories"


class DishCollection(models.Model):
  """
  A category for dishes. For example:

  Lasagna (Collection)
    Salmon Lasagna (Dish)
    Spinnace Lasagna (Dish)
    ...
  """

  name = models.CharField(max_length=100)
  categories = models.ManyToManyField(Category)
  description = models.TextField()

  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = "Dish Collections"


class Dish(models.Model):
  """
  A dish is a collection of recipe variations that all result
  in roughly the same meal to eat.
  """

  name = models.CharField(max_length=100)
  collection = models.ForeignKey(DishCollection, related_name="dishes")
  description = models.TextField()
  
  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = "Dishes"


class Ingredient(models.Model):
  """
  An ingredient is tagged in recipies and searchable. It is part of the
  creation process of a meal. It contains data for people to look up
  during cooking or while doing research into new dishes
  """

  name = models.CharField(max_length=100)
  description = models.TextField()
  
  # TODO: Add image
  # TODO: Add wikipedia information

  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = "Ingredients"


class Recipe(models.Model):
  """
  A recipe is one exact variation to make a dish
  """

  creator = models.ForeignKey(Cook)
  dish = models.ForeignKey(Dish, related_name="recipies")
  
  name = models.CharField(max_length=100)

  pub_date = models.DateTimeField('date published')
  edit_date = models.DateTimeField('date edited')
  
  instructions = models.TextField() # Json encoded for parsability
  ingredients = models.ManyToManyField(Ingredient)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = "Recipies"
