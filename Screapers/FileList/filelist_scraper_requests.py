import cloudscraper
from bs4 import BeautifulSoup

from Screapers.FileList.FilelistTorrentData import FileListTorrentData
from Screapers.IMDB.imdb_scraper import IMDBScreaper
from Screapers.settings import FileListSettings


class FileListScraper():
    '''
        class that scrapes torrents from filelist
    '''

    base_link = "https://filelist.io/"

    def log_in(self):

        login_url = self.base_link + "login.php"
        login_action_url = self.base_link + "takelogin.php"

        data = {"username": FileListSettings.user, "password": FileListSettings.password}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        self.session = cloudscraper.CloudScraper(delay=0)
        r = self.session.get(login_url, headers=headers)

        soup = BeautifulSoup(r.content, "html.parser")
        token = soup.form.input.get("value")
        data["validator"] = token

        response = self.session.post(login_action_url, data=data, headers=headers)
        if response.status_code == 200:
            print("Login sucessfully!")

    def get_query_link(self, imdb_id):
        return self.base_link + f"/browse.php?search={imdb_id}&cat=0&searchin=3&sort=2"

    def scrape(self, movie_name: str):
        self.log_in()

        query_link = self.get_query_link(IMDBScreaper().get_imdb_id(movie_name))
        query_response = self.session.get(query_link)

        return self.get_torrent_results(query_response)

    def get_torrent_information(self, soup: BeautifulSoup):
        '''
            returns a FileListTorrent given the html of one of the results of the search
        '''
        columns = soup.find_all("div", {"class": "torrenttable"})

        torrent_colum = columns[1]
        torrent_name = torrent_colum.find("b").get_text()

        images = torrent_colum.find_all("img")
        has_freeleech = any(image["alt"] == "FreeLeech" for image in images)

        download_colum = columns[3]
        download_link = self.base_link + download_colum.a["href"]

        size_colum = columns[6]
        torrent_size = size_colum.find("span").get_text()

        seeders_colum = columns[8]
        seeders = seeders_colum.find("span").get_text()

        return FileListTorrentData(
            name=torrent_name,
            download_link=download_link,
            size=torrent_size,
            seeders=seeders,
            has_freeleech=has_freeleech
        )

    def get_torrent_results(self, response):
        '''
            gets the torrent data from the query reponse
        '''
        html = BeautifulSoup(response.content, 'html.parser')
        all_soup_results = html.find_all("div", {"class": "torrentrow"})
        torrent_list = [self.get_torrent_information(soup) for soup in all_soup_results]
        if not torrent_list:
            raise Exception("Could not find any movies on filelist.io with your search")

        return torrent_list
