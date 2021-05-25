import os
import subprocess
import crayons

from MovieProject.Scrapers.Subtitles.subtitles_diactritice import run_subtitles_diactritice

# !!!! IMPORTANT daca vrei sa schimbi directorul de cautare
input_dir = r"M:\TV shows\Merlin"
dir = input_dir
movies = []
skipped = list()

movies_renamed = 0
input_answer_rename_all = str()



def change_movie_name(path, nume_initial):

    global movies_renamed
    # iau extensia in variabila ext (.mp4) -> -4 caractere
    ext = nume_initial[-4:]
    # sterg extensia si am stringul nume_final
    nume_final = nume_initial[:-4]
    # initial nu am modificat niciun nume de fisier
    gasit = False
    pos = nume_initial.find("x264")
    if pos != -1:
        # daca gasesc x264 atunci sterg totul pana la x264
        # si aduna x264 la loc + extensia deja stearsa
        gasit = True
        nume_final = nume_initial[:pos] + "x264" + ext
    if gasit:
        global input_answer_rename_all
        if input_answer_rename_all == 'y':
            movies_renamed += 1

            # ex: nume de film initial : Aquaman.2018.1080p.BluRay.x264-[YTS].mp4
            # ce vrem este sa avem M:\Movies\Aquaman (2018)\Aquaman.2018.1080p.BluRay.x264.mp4
            # sterg din path numele filmului   :-len(nume_initial)
            # si voi ramane cu un path care arata asa :
            # M:\Movies\Aquaman (2018)\
            # apoi adaug modificat care este : Aquaman.2018.1080p.BluRay.x264.mp4
            # rezullta path_sters = :\Movies\Aquaman (2018)\Aquaman.2018.1080p.BluRay.x264.mp4
            path_sters = path[:-len(nume_initial)] + nume_final
            os.rename(path,path_sters)
    else:
        skipped.append(nume_initial)

def rename_all_movies_in_dir():
    print(crayons.green("Renaming movies such that ss can find them"))
    global input_answer_rename_all
    input_answer_rename_all = input("Are you sure you want to rename all. y/n ")
    number_of_total_movies = 0
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            path = subdir + os.sep + file
            # path este path-ul curent pentru file
            # daca are extensie de .mp4,.avi,.mkv este considerat film
            if file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mkv"):
                number_of_total_movies += 1
                movies.append(file)
                change_movie_name(path, file)
    print(crayons.cyan("Modified: ") + str(movies_renamed) + "/" + str(number_of_total_movies))
    print(crayons.red("Skipped: ") + str(len(skipped)))
    for movie_skipped in skipped:
        print(movie_skipped)
    print()

def verify_if_movie_has_already_subtitle(path):
    # gasesc pozitia ultima pozitie pe care se afla \
    # M:\Movies\Ready Player One (2018)\Ready.Player.One.2018.1080p.BluRay.x264.mp4
    pos = path.rfind(os.sep)
    # dir mare o sa fie M:\Movies\Ready Player One (2018)\
    dir_mare = path[0:pos]
    # iar nume nume_film o sa fie dupa '\' si cu 4 caractere in spate
    # adica fara extensie => Ready.Player.One.2018.1080p.BluRay.x264
    nume_film = path[pos + 1:-4]

    # iterez prin fisierele direct copii ai dir mare
    for file in os.listdir(dir_mare):
        # daca exista o subitrare care acelasi nume cu filmul atunci
        # filmul are deja subtitrarea gasite
        # file[:-4] ia fara extensie
        if (file.endswith(".srt") or file.endswith(".ass")) and file[:-4] == nume_film:
            return False
    return True

def run_ss_subtitle_search():
    input_answer_override_all_subtitles = input("Do you want to override all subtitles? y/n ")
    print(crayons.cyan("Running subtitle search"))
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            path = subdir + os.sep + file

            if file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mkv"):
                if input_answer_override_all_subtitles == 'y' or verify_if_movie_has_already_subtitle(path):
                    subprocess.run(['ss', path])

def subtitles_diactritice_all():
    print(crayons.cyan("Running diacritice replace..."))
    input_answer_diactritice_all = input("Vrei sa modifici toate diacriticile. y/n ")
    if input_answer_diactritice_all == 'y':
        for subdir, dirs, files in os.walk(dir):
            for file in files:
                path = subdir + os.sep + file
                if file.endswith(".srt"):
                    print(path)
                    run_subtitles_diactritice(path)

run_ss_subtitle_search()