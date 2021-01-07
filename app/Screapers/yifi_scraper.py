import zipfile
import os
import io
import shutil
import requests as R
from Screapers.helpers import get_html_from_url

class YifiScreaper:
    def __init__(self,directory,verbose_mode = False):
        self.base_link = "https://yts-subs.com/"
        self.directory = directory
        self.verbose = verbose_mode

    def print_terminal(self, terminal_message):
        if self.verbose is True:
            print(terminal_message)

    def get_query_link(self, movie_name):
        # returnes the hthml of the page that appears after searching the movie name
        query_name = movie_name.replace(" ", "%20")
        query_link = "https://yts-subs.com/search/" + query_name
        return query_link


    def get_first_movie_link(self, query_link):
        query_html = get_html_from_url(query_link)
        first_movie_in_list = query_html.find("div", {"class": "media-body"})
        if first_movie_in_list is None:
            return None
        else:
            first_movie_link = self.base_link + first_movie_in_list.find('a')['href']
            return first_movie_link


    def get_subtitles_links(self, movie_link):
        html = get_html_from_url(movie_link)
        table_of_all_subtitles = html.find("div", {"class": "table-responsive"})

        for row in table_of_all_subtitles.find_all("tr", {"class": "high-rating"}):
            flag = row.find("td", {"class": "flag-cell"})
            language = flag.find("span", {"class": "sub-lang"}).get_text()
            link = self.base_link + row.find('a')['href']
            if language == "Romanian":
                yield link


    def get_download_links(self, movie_name):
        # returns a list with all the download links for the subtitles found

        query_link = self.get_query_link(movie_name)
        first_movie_link = self.get_first_movie_link(query_link)
        if first_movie_link is None:
            self.print_terminal("Nu am gasit deloc filmul pe site-ul yifi")
            return None
        subtitles_links = list(self.get_subtitles_links(first_movie_link))

        if len(subtitles_links) == 0:
            self.print_terminal("Nu am gasit subtitrari in romana din pacate")
            return None
        for link in subtitles_links:
            html = get_html_from_url(link)
            download_button = html.find('a', {"class": "btn-icon download-subtitle"})
            yield download_button['href']


    def download(self, link, download_path):
        path_creaza = download_path + os.sep + "subs"
        if os.path.exists(path_creaza) == False:
            os.mkdir(path_creaza)

        r = R.get(link)
        zip = zipfile.ZipFile(io.BytesIO(r.content))
        zip.extractall(path=path_creaza)
        path_sterge = path_creaza + os.sep + "__MACOSX"
        if os.path.exists(path_sterge):
            shutil.rmtree(path_sterge)


    def download_subtitles_for_movie(self, movie_name, download_path):
        download_links = list(self.get_download_links(movie_name))
        if download_links is None:
            return
        for link in download_links:
            self.print_terminal(link)
            self.download(link, download_path)