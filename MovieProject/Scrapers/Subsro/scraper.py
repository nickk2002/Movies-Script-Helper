import os
import time

from bs4 import BeautifulSoup
from pyunpack import Archive

from MovieProject.Scrapers.IMDB.scraper import IMDBScraper, IMDBScrapeMode
from MovieProject.Scrapers.MyScraperLibrary.ScraperQuery import ScaperQuery


class SubsroScraper(ScaperQuery):
    base_link = "https://subs.ro"

    def get_query_link(self, query_name):
        imdb_id = IMDBScraper().scrape(query_name, IMDBScrapeMode.ID)
        return f"/subtitrari/imdbid/{imdb_id}"

    def handle_result(self, soup: BeautifulSoup):
        download_link = soup.find("a", class_="btn-download")["href"]
        file_name = "subs.ro-" + self.query_name
        archive_path = self.download(download_link, filename=file_name, extension="zip")
        self.handle_downloaded_files(archive_path)
        return download_link

    @staticmethod
    def handle_downloaded_files(archive_path):
        while not os.path.exists(archive_path):
            time.sleep(0.5)

        subfolder_name = "Subtitles"

        movie_folder = r"E:\Quick access\Desktop\Test"
        subtitles_path = os.path.join(movie_folder, subfolder_name)

        if not os.path.exists(subtitles_path):
            os.mkdir(subtitles_path)
        try:
            Archive(archive_path).extractall(subtitles_path)
        except:
            print("Archive is not a rar file")

    def handle_query_result(self, query_url: str, soup: BeautifulSoup, scrape_enum):
        results_wrapper = soup.find("ul", class_="items")
        results = results_wrapper.find_all("li")
        first_subtitle = results[0]
        return self.handle_result(first_subtitle)


def test():
    movies = ["Thor", "Avengers", "Inception", "Mission Impossible", "Over the rainbow"]
    scraper = SubsroScraper()
    for movie in movies:
        scraper.scrape(movie)


if __name__ == "__main__":
    SubsroScraper().scrape("Once upon a time")
