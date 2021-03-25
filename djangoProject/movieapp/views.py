from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
    context = {
        "movies" : Movie.objects.all()
    }
    return render(request, "homepage.html", context)


def movie(request, id):
    context = {}
    return render(request, "movie.html", context)
