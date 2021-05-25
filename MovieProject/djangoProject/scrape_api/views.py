from django.shortcuts import render

from MovieProject.Scrapers.IMDB.exceptions import IMDB404Error
from MovieProject.Scrapers.IMDB.scrape_mode import IMDBScrapeMode
from MovieProject.Scrapers.IMDB.scraper import IMDBScraper
from MovieProject.Scrapers.Subtitles.manager import create_and_replace


def find_id(request, id):
    try:
        data = IMDBScraper().get_information(id, IMDBScrapeMode.FullScrape)
    except IMDB404Error:
        return render(request, "nomovie.html")
    context = {
        "data": data,
    }
    create_and_replace(data['id'])
    return render(request, "API/succes.html", context)


def find_name(request, movie_name):
    try:
        data = IMDBScraper().scrape(movie_name, IMDBScrapeMode.FullScrape)
    except IMDB404Error:
        return render(request, "nomovie.html")
    context = {
        "data": data,
    }
    # print(SubsroScraper().scrape(data['id']))
    return render(request, "API/succes.html", context)
