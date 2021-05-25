from dataclasses import dataclass

from colorama import Fore, Style


@dataclass
class FileListTorrentData:
    name: str
    download_link: str
    size: int
    seeders: int
    has_freeleech: bool
    download_speed: float
    duration: int

    def pretty_print(self):
        print(f'[{self.size} GB] [S:{self.seeders}] [Bitrate:{round(self.download_speed,2)}] ', end=" ")
        if self.has_freeleech:
            print(Fore.GREEN, self.name)
        else:
            print(Fore.RED, self.name)
        print(Style.RESET_ALL, end="")
