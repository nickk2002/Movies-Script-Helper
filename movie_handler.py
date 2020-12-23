import os
import argparse
import pathlib
from Screapers.yifi_screaper import YifiScreaper
from subtitles_diactritice import run_subtitle_replace_dir
from folder_rename import run_folder_rename_dir


class MovieHandler:
    def __init__(self, directory):
        self.directory = directory

    def run_subtitles_serach_yifi(self, verbose_mode):
        yifi_screaper = YifiScreaper(self.directory)
        yifi_screaper.silent = verbose_mode

        subdir = [file for file in os.scandir(self.directory) if file.is_dir()]
        print("Scaning Files:")
        for file in subdir:
            file_name = file.name
            poz = file_name.find("(")
            movie_name = file_name
            if poz != -1:
                movie_name = file_name[:poz]
            print(movie_name)
            yifi_screaper.download_subtitles_for_movie(movie_name=movie_name, download_path=file.path)

    def run_subtitles_replace(self):
        run_subtitle_replace_dir(self.directory)

    def run_folder_rename(self):
        run_folder_rename_dir(self.directory)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", "--directory", help="set the base directory for movie handling")
    parser.add_argument("-v", "--view", action='store_true')
    parser.add_argument("-yifi", "--find-yifi", action='store_true', help="find yts subtitles ")
    parser.add_argument("-di", "--diacritice", action='store_true', help="run diactritice")
    parser.add_argument("-m", "--modify-name", action='store_true', help="modify folder name to match trailer")

    args = parser.parse_args()

    if args.directory is None or not os.path.exists(args.directory):
        if args.directory is None:
            print(f"No dir provided, using default.")
        elif not os.path.exists(str(args.directory)):
            print(f"The directory provided {args.directory} does not exits!")
        args.directory = pathlib.Path(__file__).parent.absolute()
        print(f"Using the current directory {args.directory}")

    movie_handler = MovieHandler(
        directory=args.directory,
    )
    if args.find_yifi:
        movie_handler.run_subtitles_serach_yifi(args.view)
    if args.diacritice:
        movie_handler.run_subtitles_replace()
    if args.modify_name:
        movie_handler.run_folder_rename()


if __name__ == "__main__":
    main()
