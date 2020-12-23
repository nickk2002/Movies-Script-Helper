import os
import zipfile
import time
from selenium.webdriver.common.by import By
from pyunpack import Archive
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from Screapers.helpers import wait_to_load
from Scripts.movie import Movie

test_folder = "E:\Quick access\Documents\Info\Proiecte mari\Python\Movie Project\Folder Test"

'''
    Class that downloads subtitles from subs.ro based on imdb id of movie
    Chrome-driver must be installed
    7Zip must be installed https://www.7-zip.org/
'''
class SubsroScreaper():
    def __init__(self):
        self.base_link = "https://subs.ro/subtitrari/"
        self.chrome_driver_path = r"E:\Quick access\Documents\Info\Plugins\ChromeDriver\chromedriver.exe"

    def initialize_driver(self, download_path):
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': download_path,
                 "download.prompt_for_download": False}
        chrome_options.add_experimental_option('prefs', prefs)

        self.browser = webdriver.Chrome(
            executable_path=self.chrome_driver_path,
            options=chrome_options)

        self.browser.get(self.base_link)


    def download_subtitle(self, movie : Movie):
        """
        searches the movie_name on subs.ro by imdb id and
        downloads in movie folder
        """

        self.initialize_driver(movie.name)

        enter_search = wait_to_load(self.browser, By.XPATH, "//input[@type='submit']")
        enter_search.click()

        imdb_input = wait_to_load(self.browser, By.XPATH, "//input[@type='text' and @name='imdb']")
        imdb_input.send_keys(movie.imdb_id)

        seach_button = wait_to_load(self.browser, By.XPATH, "//input[@type='submit' and @value='Caută']")
        seach_button.click()

        try:
            div = wait_to_load(self.browser, By.CLASS_NAME, "sub-buttons")
            div.click()
        except TimeoutException:
            print(f"Could not find subtitles on {self.base_link} for movie '{movie.name}' ")
            return

        if not self.already_downloaded(movie.folder_path):
            download_button = wait_to_load(self.browser, By.CLASS_NAME, "btn-download")
            download_button.click()
            time.sleep(2)
            self.handle_downloaded_archive(movie.folder_path)
        else:
            print(f"The movie {movie.name} had already subtitles in directory")
        self.browser.quit()

    def get_all_archive_files(self, movie_folder):
        '''
        return a list with all the subtitles archives downloaded from subs.ro
        '''
        return list(filter(lambda file: file.startswith("www.subs.ro"), os.listdir(movie_folder)))
    def already_downloaded(self, movie_folder):
        return len(self.get_all_archive_files(movie_folder)) > 0

    def handle_downloaded_archive(self, movie_folder):
        '''
            gets the first archive in the movie folder and then extracts the subtitles
            to "Subs ro subtitles" subfolder
        '''

        subfolder_name = "Subs ro subtitles"
        all_archives = self.get_all_archive_files(movie_folder)
        if len(all_archives) == 0:
            print(f"Trying to get {self.base_link} zip in folder {movie_folder} but there are not any.")
            return

        first_archive = all_archives[0]
        archive_path = os.path.join(movie_folder, first_archive)
        subtitles_path = os.path.join(movie_folder, subfolder_name)

        if not os.path.exists(subtitles_path):
            os.mkdir(subtitles_path)
        if first_archive.endswith("zip"):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(subtitles_path)
        elif first_archive.endswith("rar"):
            Archive(archive_path).extractall(subtitles_path)

    def get_real_movie_name(self, file_name):
        """
            Removes the movie () year brackets transforming Once upon a time(2002) -> Once upon a time
        :param file_name:
        :return:
        """
        index = file_name.find("(")
        movie_name = file_name
        if index != -1:
            movie_name = file_name[:index]
        return movie_name

    def find_subtitles_recursive(self, base_directory):
        lista = [file for file in os.scandir(base_directory) if file.is_dir()]
        for file in lista:
            self.download_subtitle(Movie(file.path))


SubsroScreaper().find_subtitles_recursive(test_folder)
