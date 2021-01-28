from chardet import detect
import crayons
import os


def get_encoding_type(path):
    with open(path, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']


def change_encoding_to_utf8(path):
    code = get_encoding_type(path)
    if code == 'utf-8':
        return
    try:
        with open(path, 'r', encoding=code) as f:
            text = f.read()
        with open(path, 'w', encoding='utf-8') as e:
            e.write(text)
    except UnicodeDecodeError:
        print(crayons.red('Decode Error'))
    except UnicodeEncodeError:
        print('Encode Error')


def check_if_already_modified(path, modified_pattern):
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        for (index, line) in enumerate(file):
            # verific linia a 3 a daca contine mod
            try:
                if line.find(modified_pattern) != -1:
                    return True
                if index >= 3:
                    return False
            except:
                return False


def convert_line_diactritice(line):
    line = line.replace('º', 'ș')
    line = line.replace('þ', 'ț')
    line = line.replace('ª', 'Ș')
    return line


def run_subtitles_diactritice(path,file_name):
    if check_if_already_modified(path, "MODIFIED#0"):
        print(crayons.green(f"{file_name} is already Modified"))
        return False

    change_encoding_to_utf8(path)
    diactritice_text = str()
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            diactritice_text += convert_line_diactritice(line)

    pattern = "0\n00:00:00,000 --> 00:00:00,000\nMODIFIED#0\n\n"
    text_nou = pattern
    text_nou += diactritice_text

    with open(path, "w", encoding='utf-8') as f:
        f.write(text_nou)
    return True

def run_subtitle_replace_dir(directory):
    print(crayons.magenta("Running diacritice replace..."))

    subtitles_modifed = 0
    subtitles = 0
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            path = subdir + os.sep + file
            if file.endswith(".srt"):
                subtitles += 1
                status = run_subtitles_diactritice(path,file)
                if status:
                    subtitles_modifed += 1
    print(f"Discovered {subti}")