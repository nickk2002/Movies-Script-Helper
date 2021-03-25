from django.apps import AppConfig
import django

django.setup()

from movieapp.models import Movie


class MovieappConfig(AppConfig):
    name = 'movieapp'


print(Movie.objects.create(imdb_id=12221,name="ANa"))
