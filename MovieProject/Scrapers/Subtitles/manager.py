from MovieProject.Scrapers.Subtitles.Subsro.scraper import SubsroScraper
from MovieProject.Scrapers.Subtitles.subtitles_diactritice import run_subtitle_replace_dir
from MovieProject.Scrapers.settings import Download


def create_and_replace(query_name):
    SubsroScraper().scrape(query_name)
    run_subtitle_replace_dir(Download.download_folder)
