from enum import Enum

from django.db import models


class Titles(models.Model):
    movie_id = models.PositiveIntegerField()
    title = models.CharField(max_length=50)
    language = models.CharField(max_length=50, null=True)
    region = models.CharField(max_length=5, null=True)
    is_original = models.BooleanField()


class Movie(models.Model):
    imdb_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    moviedb_id = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=250, null=True)
    tagline = models.CharField(max_length=50)
    rating = models.FloatField(null=True)
    votes = models.PositiveIntegerField(null=True)
    popularity = models.FloatField(null=True)

    release_date = models.DateField(null=True)
    # country = models.CharField(max_length=50, null=True)
    budget = models.PositiveIntegerField(null=True)
    profit = models.PositiveIntegerField(null=True)
    duration = models.PositiveIntegerField(null=True)
    is_series = models.NullBooleanField()
    poster_path = models.CharField(null=True, max_length=100)

    # pictures = models.

    def get_year(self):
        return self.release_date.year

    def get_genres(self):
        genre_list = []
        for category in Category.objects.filter(movie_id=self.id):
            genre_list.append(Genre.objects.get(id=category.genre_id).name)
        return genre_list


class ContractType(Enum):
    DIRECTOR = "DIRECTOR"
    ACTOR = "ACTOR"
    WRITER = "WRITER"

    @classmethod
    def choices(cls):
        return tuple((field.name, field.value) for field in cls)


class Person(models.Model):
    name = models.CharField(max_length=50)
    popularity = models.FloatField()
    imdb_id = models.CharField(max_length=50, null=True)
    gender = models.IntegerField()
    bio = models.CharField(max_length=100)
    birth_place = models.CharField(max_length=50, null=True)


class Contract(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    character = models.CharField(max_length=50, null=True)
    job = models.CharField(max_length=50, null=True)


class Genre(models.Model):
    name = models.CharField(max_length=50)


class Category(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Location(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)


class LocationContract(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
