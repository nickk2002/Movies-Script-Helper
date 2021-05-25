import os

from MovieProject.Scrapers.IMDB.scraper import *


class Movie:
    def __init__(self, movie_path="", mkv_name="", movie_name=""):
        self.folder_path = movie_path
        self.mkv_name = mkv_name
        if movie_name != "":
            self.name = movie_name
        elif movie_path != "":
            self.folder_name = os.path.basename(movie_path)
            self.name = self.get_movie_name_without_year()
        self.imdb_id = IMDBScraper().scrape(self.name, IMDBScrapeMode.ID)

    def get_movie_name_without_year(self):
        return re.search("[a-zA-Z ]+", self.folder_name).group()

    def __str__(self):
        return self.name
