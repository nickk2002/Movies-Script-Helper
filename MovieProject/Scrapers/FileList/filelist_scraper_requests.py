import regex as re
from bs4 import BeautifulSoup

from MovieProject.Scrapers.FileList.FilelistTorrentData import FileListTorrentData
from MovieProject.Scrapers.IMDB.scraper import IMDBScraper, IMDBScrapeMode
from MovieProject.Scrapers.MyScraperLibrary.ScraperQuery import ScaperQuery
from MovieProject.Scrapers.settings import FileListSettings


class FileListScraper(ScaperQuery):
    """
        class that scrapes torrents from filelist
    """

    base_link = "https://filelist.io/"
    login = True
    user = FileListSettings.user
    password = FileListSettings.password

    # use_proxy = True

    def __init__(self):
        super().__init__()

    def check_good_login(self, soup: BeautifulSoup, data: dict):

        error_image = soup.find("img", src="styles/images/attention.png")
        if error_image:
            raise Exception(
                "Login failed! Filelist says too many request, comeback in an hour. \n"
                "'Numarul maxim permis de actiuni a fost depasit. Reveniti peste o ora.' :(")
        avatar = soup.find("div", {"class": "status_avatar"})
        if avatar:
            print("Login sucessfully!")
        else:
            raise Exception(f"Login failed! Check user and password set up in settings.py "
                            f"\n username: {data['username']} \n password: {data['password']} ")

    def get_query_link(self, movie_name: str):
        self.imdb_id, self.duration = IMDBScraper().scrape(movie_name, IMDBScrapeMode.ID_DURATION)
        return f"/browse.php?search={self.imdb_id}&cat=0&searchin=3&sort=2"

    def handle_torrent(self, soup: BeautifulSoup):
        """
            returns a FileListTorrent given the html of one of the results of the search
        """
        columns = soup.find_all("div", class_="torrenttable")

        torrent_colum = columns[1]
        torrent_name = torrent_colum.find("b").get_text()

        images = torrent_colum.find_all("img")
        has_freeleech = any(image["alt"] == "FreeLeech" for image in images)

        download_colum = columns[3]
        download_link = self.base_link + download_colum.a["href"]

        size_colum = columns[6]
        torrent_size = size_colum.find("span").get_text()
        torrent_size = int(re.findall("\d+", torrent_size)[0])

        seeders_colum = columns[8]
        seeders = seeders_colum.find("span").get_text()

        movie_duration = self.duration
        download_speed = 400 * torrent_size / (3 * movie_duration)

        return FileListTorrentData(
            name=torrent_name,
            download_link=download_link,
            size=torrent_size,
            seeders=seeders,
            has_freeleech=has_freeleech,
            download_speed=download_speed,
            duration=movie_duration,
        )

    def handle_query_result(self, query_url: str, soup: BeautifulSoup, scrape_enum=None):
        """
            gets the torrent data from the query reponse
        """
        all_soup_results = soup.find_all("div", {"class": "torrentrow"})
        torrent_list = [self.handle_torrent(soup) for soup in all_soup_results]
        if not torrent_list:
            raise Exception("Could not find any movies on filelist.io with your search")
        return torrent_list


if __name__ == "__main__":
    FileListScraper().scrape("Thor")
