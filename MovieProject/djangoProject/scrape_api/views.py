from django.shortcuts import render

from MovieProject.Scrapers.IMDB.exceptions import IMDB404Error
from MovieProject.Scrapers.IMDB.scrape_mode import IMDBScrapeMode
from MovieProject.Scrapers.IMDB.scraper import IMDBScraper

def find(request, id):
    try:
        IMDBScraper().get_information(id, IMDBScrapeMode.CHECK_EXISTS)
    except IMDB404Error:
        return render(request, "nomovie.html")
    context = {
        "id": id
    }
    return render(request, ".html", context)
