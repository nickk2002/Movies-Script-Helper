from dataclasses import dataclass

from colorama import Fore, Style

@dataclass
class FileListTorrentData():
    name: str
    download_link: str
    size: str
    seeders: int
    has_freeleech: bool

    def pretty_print(self):
        if self.has_freeleech:
            print(Fore.GREEN + self.name, end=" ")
        else:
            print(Fore.RED + self.name, end=" ")
        print(Style.RESET_ALL + self.size, "Seeders", self.seeders, sep=" ")