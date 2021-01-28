import django

django.setup()

import csv
from app.Scrapers.IMDB.imdb_scraper import IMDBScreaper
from movieapp.models import Movie, Title, Genretypes
from multiprocessing import Pool

class NoTitlesForMovie(Exception):
    pass


def push_movies():
    with open("movie_name.txt") as f:
        for line in f:
            movie_name = line.strip()
            try:
                data = IMDBScreaper().scrape(movie_name)
            except:
                continue
            print(data.duration.minutes)
            try:
                Movie.objects.create(
                    name=data.name,
                )
            except django.db.utils.IntegrityError:
                pass


def read_from_imdb_file(max_id):
    file_name = "E:\Quick access\Desktop\data.tsv"
    with open(file_name, encoding='ansi') as f:
        reader = csv.reader(f, delimiter="\t", quotechar='"')
        next(reader)
        for row in reader:
            imdb_id = row[0][2:]
            if int(imdb_id) > max_id:
                break
            title = row[2]
            region = row[3]
            original = row[7]
            print(row)
            try:
                movie = Movie.objects.get(imdb_id=imdb_id)
            except:
                movie = None
            Title.objects.create(movie=movie, name=title, region=region, original=original)


def get_movie_name(imdb_id):
    matched_languages = ['US', 'GB', 'FR', 'RO']
    titles = Title.objects.filter(movie__imdb_id=imdb_id)
    if not titles:
        return None
    for language in matched_languages:
        if titles.filter(region=language):
            name = titles.filter(region=language)[0].name
            return name
    return titles[0].name


def get_movie_with_id(imdb_id):
    try:
        movie = Movie.objects.get(imdb_id=imdb_id)
    except:
        movie = None
    return movie


scraper = IMDBScreaper()


def handle_movie(id):
    movie = get_movie_with_id(id)

    modified_name = get_movie_name(id)

    if not movie:
        # we don't have that movie yet
        try:
            data = scraper.get_information(id)
        except:
            print("there is no imdb at that id",id)
            return
        print("Scraped", data.name)

        movie = Movie.objects.create(
            imdb_id=data.id,
            name=data.name,
            description=data.description,
            duration=data.duration,
            genre=data.genre,
            imdb_rating=data.rating,
            votes=data.votes,
        )
    print(id)
    if modified_name != None and movie.name != modified_name:
        print(id, movie.name, ' => ', modified_name)
        movie.name = modified_name
        movie.save()

    votes_str = movie.votes
    if type(votes_str) is str:
        votes_str = votes_str.replace(",", "")
        print(votes_str)
        movie.votes = int(votes_str)
    movie.save()


def create_genre_table(id):
    movie = Movie.objects.get(imdb_id=id)
    genre_list = movie.genre.split()
    for genre in genre_list:
        Genretypes.objects.get_or_create(movie=movie, genre=genre)
    print("Created genre entries for ", id)


def scapre_imdb_to_database(max_id: int):
    pool = Pool()
    ls = list(range(1, max_id))
    pool.map(create_genre_table, ls)


def fast_operation(ls, function):
    if __name__ == "__main__":
        pool = Pool()
        pool.map(function, ls)


def save_name(movie):
    print(movie.imdb_id)
    data = scraper.get_information(movie.imdb_id)
    movie.name = data.name
    movie.save()
    print(movie.name)


# handle_movie(5)
fast_operation(range(1000, 1000000),handle_movie)
