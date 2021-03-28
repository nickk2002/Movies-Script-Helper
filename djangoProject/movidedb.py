from typing import Type

import django

django.setup()

import requests
from django.db.models import Model
from movieapp.models import *

api_key = "6d6d1df672c9b7b8a3c432a018b38570"


def get_json(url):
    return requests.get(url).json()


def get_result_ids(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={query}&page=1&include_adult=false"
    info = requests.get(url).json()
    results = []
    for result in info['results']:
        results.append(result['id'])
    return results


def get_movies_by_votes():
    url = f"https://api.themoviedb.org/3/discover/movie?sort_by=vote_count.desc&api_key={api_key}"
    info = requests.get(url).json()
    results = [result['id'] for result in info['results']]
    return results


def update_or_create(model: Type[Model], safety_check, **kwargs):
    if model.objects.filter(**safety_check):
        old_entry = model.objects.filter(**safety_check)
        old_entry.update(**kwargs)
        return (model.objects.get(**safety_check), False)
    new_created = model.objects.create(**kwargs)
    print(f"Created {model.__name__}")
    return (new_created, True)


def push_to_db(data):
    movie, status = update_or_create(
        model=Movie,
        safety_check={
            "moviedb_id": data['id']
        },
        imdb_id=data['imdb_id'],
        moviedb_id=data['id'],
        name=data['title'],
        description=data['overview'],
        tagline=data['tagline'],
        rating=data['vote_average'],
        popularity=data['popularity'],
        votes=data['vote_count'],
        release_date=data['release_date'],
        budget=data['budget'],
        profit=data['revenue'],
        duration=data['runtime'],
    )
    for genre_data in data['genres']:
        genre, status = update_or_create(model=Genre,
                                         safety_check={"name": genre_data['name']},
                                         name=genre_data['name'])
        Category.objects.get_or_create(movie=movie, genre=genre)
    for location_data in data['production_countries']:
        location, status = Location.objects.get_or_create(
            short_name=location_data['iso_3166_1'],
            name=location_data['name'])
        LocationContract.objects.get_or_create(movie=movie, location=location)
    cast_url = f"https://api.themoviedb.org/3/movie/{data['id']}/credits?api_key={api_key}"
    print(cast_url)
    actor_data = requests.get(cast_url).json()
    for cast_member in actor_data['cast']:
        person_id = cast_member['id']
        person_data = get_json(f"https://api.themoviedb.org/3/person/{person_id}?api_key={api_key}")

        person, status = update_or_create(
            model=Person,
            safety_check={
                "name": person_data['name']
            },
            name=person_data['name'],
            popularity=person_data['popularity'],
            imdb_id=person_data['imdb_id'],
            gender=person_data['gender'],
            bio=person_data['biography'],
            birth_place=person_data["place_of_birth"],
            image_path=person_data["profile_path"]
        )
        Contract.objects.get_or_create(
            movie=movie,
            person=person,
            department=cast_member["known_for_department"],
            character=cast_member["character"]
        )
    for crew_member in actor_data['crew']:
        person_id = crew_member['id']
        person_data = get_json(f"https://api.themoviedb.org/3/person/{person_id}?api_key={api_key}")
        person, status = update_or_create(
            model=Person,
            safety_check={
                "name": person_data['name']
            },
            name=person_data['name'],
            popularity=person_data['popularity'],
            imdb_id=person_data['imdb_id'],
            gender=person_data['gender'],
            bio=person_data['biography'],
            birth_place=person_data["place_of_birth"],
            image_path=person_data["profile_path"]
        )
        Contract.objects.get_or_create(
            movie=movie,
            person=person,
            department=crew_member["department"],
            job=crew_member["job"]
        )


def remove_movie_duplicates():
    movies = Movie.objects.order_by("imdb_id")
    cnt = 0
    for movie in movies:
        cnt += 1
        if cnt % 2 == 0:
            print("deleting", movie.name, movie.id)
            Movie.objects.filter(id=movie.id).delete()


def run_movies():
    result_ids = get_movies_by_votes()
    for movie_id in result_ids[:10]:
        data = get_json(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}")
        movie = Movie.objects.get(moviedb_id=movie_id)
        push_to_db(data)
        images = get_json(
            f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={api_key}&include_image_language=en,null")
        posters = images['posters']
        posters.sort(key=lambda x: (x['vote_average'], x['vote_count']), reverse=True)
        first_image = images['posters'][0]

        backdrops = images['backdrops']
        backdrops.sort(key=lambda x: (x['vote_average'], x['vote_count']), reverse=True)
        first_background = backdrops[0]

        image_url = f"https://image.tmdb.org/t/p/original{first_image['file_path']}"
        background_url = f"https://image.tmdb.org/t/p/original{first_background['file_path']}"
        print(data['title'], image_url, background_url)
        movie.poster_path = first_image['file_path']
        movie.background_path = first_background['file_path']
        # print(json.dumps(backdrops, indent=5))
        movie.save()

# Person.objects.all().delete();
run_movies()