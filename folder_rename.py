import os

import regex as re


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def modify_name(name):
    renamed = str()
    i = 0
    while i < len(name):
        letter = name[i]

        if is_int(name[i]) and is_int(name[i + 1]) and is_int(name[i + 2]) and is_int(name[i + 3]):
            if name[i - 1] != '(':
                renamed += '('

            renamed += name[i:i + 4]
            renamed += ')'
            break
        if name[i] == '.':
            j = i
            while name[j] == '.':
                j += 1
            cnt = j - i
            if j - i == 1:
                renamed += ' '
            else:
                renamed += name[i:j]
            i = j - 1
        else:
            renamed += letter
        i += 1
    return renamed


def modify_name_regex(name):
    pattern_number = "\d+"
    year = re.findall(pattern_number, name)

    pattern_letters = "[A-Za-z ]+"
    first_match = re.search(pattern_letters, name).end()

    puncte = "\.{0}(\.{3})?"
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
    if answer == 'Y':
        for (nume_folder, path) in directory_files:
            renamed_folder_name = modify_name_regex(nume_folder)
            if nume_folder != renamed_folder_name:
                path_modificat = path.replace(nume_folder, renamed_folder_name)
                os.rename(path, path_modificat)
