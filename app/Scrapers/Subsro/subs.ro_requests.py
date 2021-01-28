import os
import zipfile

from bs4 import BeautifulSoup
from pyunpack import Archive
import time
from Scrapers.IMDB.imdb_scraper import IMDBScreaper,IMDBScrapeMode
from Scrapers.MyScraperLibrary.ScraperQuery import ScaperQuery


class SubsroScraper(ScaperQuery):
    base_link = "https://subs.ro"


    def get_query_link(self, query_name):
        imdb_id = IMDBScreaper().scrape(query_name,IMDBScrapeMode.ID)
        return f"/subtitrari/imdbid/{imdb_id}"

    def handle_result(self, soup: BeautifulSoup):
        download_link = soup.find("a", class_="btn-download")["href"]
        file_name = "subs.ro-" + self.query_name
        print(file_name)
        archive_path = self.download(download_link, filename=file_name, extension="zip")
        time.sleep(3)
        self.handle_downloaded_files(archive_path)
        return download_link

    def handle_downloaded_files(self,archive_path):
        subfolder_name = "Subs ro subtitles"

        movie_folder = r"E:\Quick access\Downloads"
        subtitles_path = os.path.join(movie_folder, subfolder_name)
        print(archive_path)
        if not os.path.exists(subtitles_path):
            os.mkdir(subtitles_path)
        if archive_path.endswith("zip"):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(subtitles_path)
        elif archive_path.endswith("rar"):
            Archive(archive_path).extractall(subtitles_path)

    def handle_query_result(self, query_url: str, soup: BeautifulSoup, id):
        results_wrapper = soup.find("ul", class_="items")
        results = results_wrapper.find_all("li")
        first_subtitle = results[0]
        return self.handle_result(first_subtitle)

def fixBadZipfile(zipFile):
    f = open(zipFile, 'r+b')
    data = f.read()
    pos = data.find(b'\x50\x4b\x05\x06') # End of central directory signature
    if (pos > 0):
        print("Trancating file at location " + str(pos + 22)+ ".")
        f.seek(pos + 22)   # size of 'ZIP end of central directory record'
        f.truncate()
        f.close()
    else:
        raise Exception("Bad zip oof")

# SubsroScraper().scrape("Thor")
path = r'E:\Quick access\Downloads\subs.ro-Thor.zip'
fixBadZipfile(path)
SubsroScraper().handle_downloaded_files(path)