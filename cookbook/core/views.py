from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("This is where the cookbook index will one day be!")


