import json

import django

django.setup()

import requests
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


def push_to_db(data):
    movie, status = Movie.objects.get_or_create(
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
        genre, status = Genre.objects.get_or_create(name=genre_data['name'])
        Category.objects.get_or_create(movie=movie, genre=genre)
    for location_data in data['production_countries']:
        # print(movie.name,location_data)
        location, status = Location.objects.get_or_create(
            short_name=location_data['iso_3166_1'],
            name=location_data['name'])
        LocationContract.objects.get_or_create(movie=movie, location=location)
    cast_url = f"https://api.themoviedb.org/3/movie/{data['id']}/credits?api_key={api_key}"
    actor_data = requests.get(cast_url).json()
    # for cast_member in actor_data['cast']:
    #     person_id = cast_member['id']
    #     print(person_id)
    #     person_data = get_json(f"https://api.themoviedb.org/3/person/{person_id}?api_key={api_key}")
    #     print(person_data['imdb_id'])
    #     person, status = Person.objects.get_or_create(
    #         name=person_data['name'],
    #         popularity=person_data['popularity'],
    #         imdb_id=person_data['imdb_id'],
    #         gender=person_data['gender'],
    #         bio=person_data['biography'],
    #         birth_place=person_data["place_of_birth"]
    #     )
    #     Contract.objects.get_or_create(
    #         movie=movie,
    #         person=person,
    #         department=cast_member["known_for_department"],
    #         character=cast_member["character"]
    #     )
    # for crew_member in actor_data['crew']:
    #     person_id = crew_member['id']
    #     print(person_id)
    #     person_data = get_json(f"https://api.themoviedb.org/3/person/{person_id}?api_key={api_key}")
    #     print(person_data['imdb_id'])
    #     person, status = Person.objects.get_or_create(
    #         name=person_data['name'],
    #         popularity=person_data['popularity'],
    #         imdb_id=person_data['imdb_id'],
    #         gender=person_data['gender'],
    #         bio=person_data['biography'],
    #         birth_place=person_data["place_of_birth"]
    #     )
    #     Contract.objects.get_or_create(
    #         movie=movie,
    #         person=person,
    #         department=crew_member["department"],
    #         job=crew_member["job"]
    #     )


def run_movies():
    result_ids = get_movies_by_votes()
    for movie_id in result_ids[:10]:
        data = get_json(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}")
        movie = Movie.objects.get(moviedb_id=movie_id)
        # push_to_db(data)
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
        print(json.dumps(backdrops, indent=5))
        movie.save()


run_movies()
