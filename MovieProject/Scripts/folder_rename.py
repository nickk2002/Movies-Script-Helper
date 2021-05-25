import os

import crayons
import regex as re


def modify_name_regex(name):
    pattern_number = r"\d+"
    year = re.findall(pattern_number, name)

    pattern_letters = r"[A-Za-z ]+"
    first_match = re.search(pattern_letters, name).end()

    puncte = r"\.{0}(\.{3})?"
    puncte_final = re.findall(puncte, name[first_match:])[0]

    current_name = name[:first_match] + puncte_final
    if len(year) > 0:
        current_name += f'({year[0]})'
    return current_name


def run_folder_rename_dir(directory):
    directory_files = [(file.name, file.path) for file in os.scandir(directory) if file.is_dir()]

    for (nume_folder, path) in directory_files:
        renamed_folder_name = modify_name_regex(nume_folder)
        print(nume_folder, "=>", renamed_folder_name)
    answer = input("Do you really want to modify the names? y/n ")
    if answer == 'y' or answer == 'Y':
        print(crayons.green("Ok! Now we will modify!"))
        for (nume_folder, path) in directory_files:
            renamed_folder_name = modify_name_regex(nume_folder)
            if nume_folder != renamed_folder_name:
                path_modificat = path.replace(nume_folder, renamed_folder_name)
                print(crayons.normal(f'{nume_folder} -> {renamed_folder_name}'))
                os.rename(path, path_modificat)
