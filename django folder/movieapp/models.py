from enum import Enum

from django.db import models


# Create your models here.

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField(default=None, null=True)
    rating = models.FloatField(default=0, null=True)
    votes = models.IntegerField(default=True, null=True)
    reviews = models.IntegerField(default=None, null=True)
    description = models.CharField(max_length=200, null=True)
    release_day = models.DateField(default=None, null=True)
    country = models.CharField(max_length=50, default=None, null=True)
    language = models.CharField(max_length=50, default=None, null=True)
    budget = models.PositiveIntegerField(default=None, null=True)
    total_gross = models.PositiveIntegerField(default=None, null=True)
    duration = models.IntegerField(default=0, null=True)
    is_series = models.NullBooleanField(default=False)


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CharField)


class Personality(models.Model):
    id = models.AutoField(primary_key=True)
    imdb_id = models.IntegerField()
    name = models.CharField(max_length=50)


class ContractType(Enum):
    DIRECTOR = "DIRECTOR",
    ACTOR = "ACTOR",
    WRITER = "WRITER",

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)


class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    personality = models.ForeignKey(Personality, on_delete=models.CASCADE)
    contract_type = models.CharField(max_length=250, choices=ContractType.choices())
    star = models.NullBooleanField(default=False)
    role = models.CharField(max_length=200,null=True)


class FilmingLocation(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=250)


class LocationContract(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    filming_location = models.ForeignKey(FilmingLocation, on_delete=models.CASCADE)


class Title(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    region = models.CharField(max_length=4)
    original = models.BooleanField(default=False)
