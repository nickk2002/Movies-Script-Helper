import os
from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable

import requests
from bs4 import BeautifulSoup
from fp.fp import FreeProxy

from Scrapers.settings import Download

class ScraperMode:
    pass


@dataclass
class ScaperQuery():
    base_link = "www.example.com"

    login = False
    user = "user"
    password = "pass"
    use_proxy = False

    use_session = False
    use_requests = True

    debug = False
    download_dir = Download.download_folder

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }

    def __init__(self):
        if self.debug:
            print(
                f"Warning! You are running  {self.__class__.__name__} scraper in debug mode which means it will save html files to make queries faster"
                f"on the same web page ")
            self.cached_number = 0
        self.query_name = ""
        self.session = requests.session()  # create a session
        self.session.headers = self.headers

        if self.use_proxy:
            proxy = FreeProxy(rand=True).get()
            print(f"USing proxi {proxy}")
            self.session.proxies = {
                "http": proxy,
            }

    def parse_url(self, url):
        if not url.startswith(self.base_link):
            url = self.base_link + url  # ad the base_link to make it obsolute
        return url

    def get_or_create_debug_html(self, url, request):
        curdir = os.getcwd()
        folder_name = "Debug"
        debug_folder = os.path.join(curdir, folder_name)
        if not os.path.exists(debug_folder):
            os.mkdir(debug_folder)

        paramenters = url.replace(self.base_link + '/', "").replace("?","")
        print("Splitting", paramenters)
        file_name = f'{self.query_name} cached {paramenters}.html'
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

    def get_soup_from_url(self, url: str, data=None):
        url = self.parse_url(url)
        request = self.session.get(url, data=data)
        if request.status_code == 404:
            raise Exception(f"Request to {url} gives 404 error!")
        request_content = request.content
        if self.debug:
            request_content = self.get_or_create_debug_html(url, request)
        return BeautifulSoup(request_content, "lxml")

    def split_query_name(self, query_name: str):
        return query_name.replace(" ", "+")

    def check_good_login(self, soup : BeautifulSoup, data: dict):
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

    def scrape(self, query_name: str, scrape_enum = 0):
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
    def handle_query_result(self, query_url: str, soup: BeautifulSoup, scrape_enum = 0):
        pass

    def filter_result(self, html: BeautifulSoup):
        pass
