import os

from Scrapers.FileList.FilelistTorrentData import FileListTorrentData
from Scrapers.FileList.filelist_scraper_requests import FileListScraper
from Scrapers.settings import Download


class FileListDownloader:
    download_dir = Download.download_folder

    def __init__(self):
        self.scraper = FileListScraper()

    def run_shell(self):
        movie_name = self.ask_for_movie_name()

        torrent_list = self.scraper.scrape(movie_name)
        self.print_user_options(torrent_list)

        option = self.get_user_option(number_of_torrents=len(torrent_list))
        self.download_torrent(torrent_list[option])

    @staticmethod
    def ask_for_movie_name():
        movie_name = input("enter a movie name to download from filelist.io ")
        return movie_name

    @staticmethod
    def print_user_options(torrent_list):
        for (index, available_torrent) in enumerate(torrent_list):
            print(index, end="  ")
            available_torrent.pretty_print()

    @staticmethod
    def get_user_option(number_of_torrents):
        while True:
            try:
                user_input = input("Chose option number : ")
                if user_input == 'quit':
                    exit(0)
                option_id = int(user_input)
                if option_id >= number_of_torrents:
                    print(f"Please select an integere from range 0-{number_of_torrents - 1}")
                else:
                    return option_id
            except ValueError:
                print("Please put an integer value")

    def download_torrent(self, torrent: FileListTorrentData):
        print(f"downloading from {torrent.download_link} to {self.download_dir}")
        name = torrent.name

        with open(self.download_dir + os.sep + name + ".torrent", 'wb') as f:
            content = self.scraper.session.get(torrent.download_link).content
            f.write(content)

if __name__ == "__main__":
    FileListDownloader().run_shell()