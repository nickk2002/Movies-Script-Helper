from django.shortcuts import render, get_object_or_404

from .models import *


# Create your views here.

def index(request):
    context = {
        "movies": Movie.objects.all()
    }
    return render(request, "homepage.html", context)


def movie(request, id):
    context = {"movie": get_object_or_404(Movie, id=id)}
    return render(request, "movie.html", context)


def advanced_search(request):
    genre_list = []
    for genre in Genre.objects.all():
        genre_name = genre.name
        if genre_name == "Science Fiction":
            genre_name = "Fiction"
        genre_list.append(genre_name)
    context = {
        "genres": genre_list
    }
    return render(request, "advancedserach.html", context)


def search(request):
    info = request.GET.dict()
    name = info.get("movie name")
    rating_low = info.get("rating small")
    rating_high = info.get("rating big")
    actor_query = info.get("actor")
    movies = Movie.objects.filter(name__icontains=name, rating__range=(rating_low, rating_high))
    print(movies)
    new_movies = []
    for movie in movies:
        for actor_name in movie.get_actor_names():
            if actor_query in actor_name:
                new_movies.append(movie)
                print(actor_name)
                break
    movies = new_movies
    if movies:
        context = {
            "movies": movies,
        }
    else:
        return render(request, "404.html")
    print("Search request", info)
    return render(request, "searchresults.html", context)
