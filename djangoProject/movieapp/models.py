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
    background_path = models.CharField(null=True, max_length=100)

    def get_year(self):
        return self.release_date.year

    def get_genres_parsed(self):
        genre_list = []
        for category in Category.objects.filter(movie_id=self.id):
            genre_name = Genre.objects.get(id=category.genre_id).name
            if genre_name == "Science Fiction":
                genre_name = "SF"
            genre_list.append(genre_name)
        return genre_list

    def get_genres(self):
        genre_list = []
        for category in Category.objects.filter(movie_id=self.id):
            genre_name = Genre.objects.get(id=category.genre_id).name
            genre_list.append(genre_name)
        return genre_list

    def get_directors(self):
        director_contracts = Contract.objects.filter(movie_id=self.id, job="Director")
        directors = []
        for contract in director_contracts:
            director = Person.objects.get(id=contract.person_id)
            directors.append(director.name)
        return directors

    def get_actors(self):
        actor_list = []
        for contract in Contract.objects.filter(movie_id=self.id):
            person = Person.objects.get(id=contract.person_id)
            actor_list.append((person, contract.character))
        return actor_list

    def get_actor_names(self):
        actor_list = []
        for contract in Contract.objects.filter(movie_id=self.id):
            person = Person.objects.get(id=contract.person_id)
            actor_list.append(person.name)
        return actor_list

    def has_actor(self, actor_query):
        for actor_name in self.get_actor_names():
            if actor_query in actor_name:
                print("Matched actor", actor_name)
                return True
        return False

    def has_director(self, director_query):
        for director_name in self.get_directors():
            if director_query in director_name:
                print("Matched Direcor", director_name)
                return True
        return False

    def has_genre(self, genre_list: list):

        movie_genres = self.get_genres()
        for genre_name in genre_list:
            if genre_name in movie_genres:
                print("all genres:", movie_genres)
                return True
        return False


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
    image_path = models.CharField(max_length=50, null=True)


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
