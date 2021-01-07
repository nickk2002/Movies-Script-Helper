import os

import regex as re

from Screapers.IMDB.imdb_scraper import IMDBScreaper


class Movie:
    def __init__(self, movie_path="", mkv_name="", movie_name=""):
        self.folder_path = movie_path
        self.mkv_name = mkv_name
        if movie_name != "":
            self.name = movie_name
        elif movie_path != "":
            self.folder_name = os.path.basename(movie_path)
            self.name = self.get_movie_name_without_year()
        self.imdb_id = IMDBScreaper().get_imdb_id(movie_name=self.name)

    def get_movie_name_without_year(self):
        return re.search("[a-zA-Z ]+", self.folder_name).group()

    def __str__(self):
        return self.name

# movie = Movie("E:\Quick access\Documents\Info\Proiecte mari\Python\Movie Project\Folder Test\Once upon a time...(2002)","")
# movie.get_movie_name_without_year()
