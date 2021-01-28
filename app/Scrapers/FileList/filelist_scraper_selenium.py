import crayons
from bs4 import BeautifulSoup
from colorama import Fore, Style
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from Scrapers.helpers import wait_to_load
from Scripts.movie import Movie


class FileListTorrent():
    """
        class that handler printing a torrent to the screen
    """

    def __init__(self, torrent_info):
        self.torrent_info = torrent_info
        self.download_button = torrent_info["download_button"]

    def __str__(self):
        output = ""
        if self.torrent_info["has_freeleech"]:
            output += crayons.red(self.torrent_info["name"])
        else:
            output += crayons.red(self.torrent_info["name"])
        output += " " + self.torrent_info["size"]
        output += " " + self.torrent_info["seeders"]
        return output

    def pretty_print(self):
        if self.torrent_info["has_freeleech"]:
            print(Fore.GREEN + self.torrent_info["name"], end=" ")
        else:
            print(Fore.RED + self.torrent_info["name"], end=" ")
        print(Style.RESET_ALL + self.torrent_info["size"], "Seeders", self.torrent_info["seeders"], sep=" ")


class FileListScraper():
    """
        class that scrapes torrents from filelist
    """

    def __init__(self):
        self.base_link = "https://filelist.io/"

    def initialize_selenium(self):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values': {'images': 2}}
        options.add_experimental_option('prefs', prefs)
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        self.browser = webdriver.Chrome(executable_path=config("CHROME_DRIVER"))
        self.browser.get(self.base_link)

    def log_in(self):

        user = wait_to_load(self.browser, By.ID, "username")
        user.send_keys(config("FILELIST_USER"))
        password = self.browser.find_element_by_id("password")
        password.send_keys(config("FILELIST_PASSWORD"))
        log_in_any_ip = self.browser.find_element_by_name("unlock")
        log_in_any_ip.click()
        log_in_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        log_in_button.click()

    def get_query_link(self, imdb_id):
        return self.base_link + f"/browse.php?search={'tt' + imdb_id}&cat=0&searchin=1&sort=2"

    def scrape(self, movie):
        self.initialize_selenium()
        self.log_in()
        query_link = self.get_query_link(movie.imdb_id)
        self.browser.get(query_link)

        torrent_list = self.get_torrent_results()
        option_id = self.handle_user_input(len(torrent_list))
        self.download_torrent(torrent_list[option_id])

    def get_torrent_information(self, soup: BeautifulSoup, selenium: WebElement):
        """
            returns a FileListTorrent given the html of one of the results of the search
        """
        columns = soup.find_all("div", {"class": "torrenttable"})

        torrent_colum = columns[1]
        torrent_name = torrent_colum.find("b").get_text()

        has_freeleech = False
        images = torrent_colum.find_all("img")
        if len(images) > 0:
            freeleech = list(filter(lambda image: image["alt"] == "FreeLeech", images))
            has_freeleech = len(freeleech) > 0

        download_button = selenium.find_element_by_xpath("//img")
        print(selenium.get_attribute("innerHTML"))
        size_colum = columns[6]
        torrent_size = size_colum.find("span").get_text()

        seeders_colum = columns[8]
        seeders = seeders_colum.find("span").get_text()

        result_info = {
            "name": torrent_name,
            "download_button": download_button,
            "has_freeleech": has_freeleech,
            "size": torrent_size,
            "seeders": seeders,
        }

        return FileListTorrent(result_info)

    def get_torrent_results(self, locally=False):
        """
            gets the html from the current query page and itereates through all the results
        """
        if locally:
            html = BeautifulSoup(open("source.html"), "html.parser")
        else:
            html = BeautifulSoup(self.browser.page_source, 'html.parser')
        all_soup_results = html.find_all("div", {"class": "torrentrow"})
        all_selenium_results = self.browser.find_elements_by_class_name("torrentrow")
        torrent_list = [self.get_torrent_information(soup, selenium) for (soup, selenium) in
                        zip(all_soup_results, all_selenium_results)]

        for (index, torrent) in enumerate(torrent_list):
            print("Option ", index, end=" ")
            torrent.pretty_print()
        return torrent_list

    def handle_user_input(self, number_of_torrents):
        while True:
            try:
                option_id = int(input("Chose option number : "))
                if option_id >= number_of_torrents:
                    print(f"Please select an integere from range 0-{len(number_of_torrents) - 1}")
                else:
                    return option_id
            except ValueError:
                print("Please put an integer value")

    def download_torrent(self, torrent: FileListTorrent):
        torrent.download_button.click()
        print(torrent.download_button)
        print("Trying to download")


if __name__ == "__main__":
    FileListScraper().scrape(Movie(movie_name="Thor"))
