import os
import random
from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable

import requests
from bs4 import BeautifulSoup
from fp.fp import FreeProxy
from scraper_api import ScraperAPIClient

from Scrapers.settings import Download


@dataclass
class ScaperQuery:
    base_link = "www.example.com"

    login = False
    user = "user"
    password = "pass"
    use_proxy = False

    use_scraperapi = False

    debug = False
    download_dir = Download.download_folder

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36",
    }
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

    proxies = [

    ]

    def __init__(self):
        if self.debug:
            print(
                f"Warning! You are running  {self.__class__.__name__} scraper in debug mode which means it will save html files to make queries faster"
                f"on the same web page ")
            self.cached_number = 0
        self.query_name = ""
        self.session = requests.session()  # create a session
        self.session.headers = self.headers
        if self.use_scraperapi:
            self.client = ScraperAPIClient('827a189a13edb3490a8ea907a6f61d47')

        if self.use_proxy:
            proxy = FreeProxy(rand=True).get()
            print(f"USing proxy {proxy}")
            self.session.proxies = {
                "http": proxy,
            }
        if self.proxies:
            self.session.proxies = {
                "https": self.proxies[0]
            }
            print("Using custom proxy", self.proxies[0])

    def parse_url(self, url):
        if not url.startswith(self.base_link):
            url = self.base_link + url  # ad the base_link to make it absolute
        return url

    def get_or_create_debug_html(self, url, request):
        curdir = os.getcwd()
        folder_name = "Debug"
        debug_folder = os.path.join(curdir, folder_name)
        if not os.path.exists(debug_folder):
            os.mkdir(debug_folder)

        parameters = url.replace(self.base_link + '/', "").replace("?", "")
        print("Splitting", parameters)
        file_name = f'{self.query_name} cached {parameters}.html'
        html_file = os.path.join(debug_folder, file_name)
        print(html_file)

        if not os.path.exists(html_file):
            print(f"For request GET {url} creating file")
            print("Saved file", file_name)
            content = request.content
            with open(html_file, 'wb') as file:
                file.write(content)
        else:
            print(f"For request GET {url} using cached {file_name}")
            with open(html_file, 'r', encoding="ansi") as file:
                content = file.read()
        return content

    def rotate_agents(self):
        user_agent = random.choice(self.user_agent_list)
        self.headers['User-Agent'] = user_agent

    def get_soup_from_url(self, url: str, data=None):
        self.rotate_agents()
        url = self.parse_url(url)
        if not self.use_scraperapi:
            print(f"Using basic requests get on {url}")
            request = self.session.get(url, data=data)
        else:
            request = self.client.get(url)
        request_content = request.content
        if self.debug:
            request_content = self.get_or_create_debug_html(url, request)
        return BeautifulSoup(request_content, "lxml")

    @staticmethod
    def split_query_name(query_name: str):
        return query_name.replace(" ", "+")

    def check_good_login(self, soup: BeautifulSoup, data: dict):
        pass

    def log_in(self, user, password):
        self.session.get(self.base_link)  # first get the base link

        data = {"username": user, "password": password}

        soup = self.get_soup_from_url(self.base_link)
        login_action_url = self.base_link + soup.form["action"]
        token = soup.form.input.get("value")
        data['validator'] = token

        self.session.post(login_action_url, data=data, headers=self.headers)

        # check if the login was ok, this should be implemented by the user
        self.check_good_login(
            soup=self.get_soup_from_url(self.base_link),
            data=data)  # will raise exception if the login failed

    def scrape(self, query_name: str, scrape_enum=0):
        self.query_name = query_name

        if self.login:
            self.log_in(self.user, self.password)
        if query_name:
            queryable_name = self.split_query_name(query_name)
            query_url = self.parse_url(self.get_query_link(queryable_name))
            print(query_url)
            return self.handle_query_result(query_url, self.get_soup_from_url(query_url), scrape_enum)

    def get_url(self, url, callback: Callable[[str, BeautifulSoup], dataclass()]):
        return callback(url, self.get_soup_from_url(url))

    def download(self, download_link: str, filename: str, extension, download_dir=None):
        download = self.download_dir
        if download_dir:
            download = download_dir
        print(f"downloading from {download_link} to {download} with name {filename}")
        file_path = self.download_dir + os.sep + filename + f".{extension}"
        with open(self.download_dir + os.sep + filename + f".{extension}", 'wb') as f:
            content = self.session.get(download_link).content
            f.write(content)
        return file_path

    @abstractmethod
    def get_query_link(self, query_name):
        pass

    @abstractmethod
    def handle_query_result(self, query_url: str, soup: BeautifulSoup, scrape_enum):
        pass

    def filter_result(self, html: BeautifulSoup):
        pass
