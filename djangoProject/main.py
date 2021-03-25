import csv

import django

django.setup()

from django.core.exceptions import ValidationError
from movieapp.models import *

import regex as re


class NotNumber(Exception):
    pass


def parse_integer(input):
    if input is None:
        return None
    try:
        number = re.findall(r"\d+", input)[0]
        return int(number)
    except IndexError:
        raise NotNumber(f"The input {input} can't be parsed into a number")


tsv_file = open("E:\Quick access\Desktop\data.tsv", encoding='ansi')
read_tsv = csv.reader(tsv_file, delimiter="\t")
preffered_languages = ["US", "GB", "EN", "RO", "FR"]

Titles.objects.all().delete()

for (titleId, ordering, title, region, language, types, attributes, is_original_title) in read_tsv:
    try:
        imdb_id = parse_integer(titleId)
    except NotNumber:
        continue

    if is_original_title == '1':
        try:
            Titles.objects.get_or_create(movie_id=imdb_id, title = title, language=language, region=region, is_original=is_original_title)
        except ValidationError:
            continue
    print(region,title)
    if region in preffered_languages:
        try:
            Titles.objects.get_or_create(movie_id=imdb_id, title = title,language=language, region=region, is_original=is_original_title)
        except ValidationError:
            continue
