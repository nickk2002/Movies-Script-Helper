import os

from Screapers.FileList.FilelistTorrentData import FileListTorrentData
from Screapers.FileList.filelist_scraper_requests import FileListScraper


class FileListDownloader():
    download_dir = "E:\Quick access\Downloads"

    def __init__(self):
        self.scraper = FileListScraper()
        self.cli_manager()

    def cli_manager(self):
        movie_name = self.ask_for_movie_name()

        torrent_list = self.scraper.scrape(movie_name)
        self.print_user_options(torrent_list)

        option = self.get_user_option(number_of_torrents=len(torrent_list))
        self.download_torrent(torrent_list[option])

    def ask_for_movie_name(self):
        movie_name = input("enter a movie name to download from filelist.io ")
        return movie_name

    def print_user_options(self, torrent_list):
        for (index, available_torrent) in enumerate(torrent_list):
            print(f"Option: {index}", end=" ")
            available_torrent.pretty_print()

    def get_user_option(self, number_of_torrents):
        while True:
            try:
                option_id = int(input("Chose option number : "))
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