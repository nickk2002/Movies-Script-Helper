from MovieProject.Scrapers.IMDB.scrape_mode import IMDBScrapeMode
from MovieProject.Scrapers.IMDB.scraper import IMDBScraper
from MovieProject.Scrapers.Subtitles.Subsro import SubsroScraper

movie_name = "Thor"
data = IMDBScraper().scrape(movie_name, IMDBScrapeMode.FullScrape)
print(SubsroScraper().scrape(data['id']))