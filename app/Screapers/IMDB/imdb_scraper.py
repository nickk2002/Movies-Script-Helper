from dataclasses import dataclass

import regex as re

from Screapers.helpers import get_html_from_url


@dataclass
class IMDBData:
    id: str
    rating: float
    duration: str
    votes: int


class IMDBScreaper():
    base_link = "https://www.imdb.com"

    def get_query_link(self, movie_name):
        return f"{self.base_link}/find?q={movie_name}"

    @staticmethod
    def check_good_header(header_div):
        header_name = header_div.find("h3", {"class": "findSectionHeader"}).get_text()
        return header_name == "Titles"

    @staticmethod
    def query_name(movie_name: str):
        return movie_name.replace(" ", "+")

    def get_first_link_result(self, movie_name):
        query_name = self.query_name(movie_name)
        query_link = self.get_query_link(query_name)
        html = get_html_from_url(query_link)

        all_headers = html.find_all("div", {"class": "findSection"})
        movie_headings = list(filter(lambda header_div: self.check_good_header(header_div), all_headers))
        if len(movie_headings) == 0:
            raise Exception(f"No movies found on {self.base_link} with the name '{movie_name}'")
        first_movie_header = movie_headings[0]

        result = first_movie_header.find("td", {"class": "result_text"})  # get the first movie restul
        movie_link = result.find('a')['href']
        return self.base_link + movie_link

    def get_imdb_id(self, movie_name) -> int:
        movie_link = self.get_first_link_result(movie_name)
        imdb_id = re.findall("\d+", movie_link)[0]
        return imdb_id

    def run_scraper(self, movie_name) -> IMDBData:
        movie_link = self.get_first_link_result(movie_name)
        print(movie_link)

        html = get_html_from_url(movie_link)
        imdb_id = re.findall("\d+", movie_link)[0]
        rating_class = html.find("div", {"class": "imdbRating"})
        rating = rating_class.find("strong").get_text()
        nr_votes = rating_class.find("span", {"class": "small"}).get_text()

        subtext = html.find("div", {"class": "subtext"})
        duration = subtext.find("time").get_text().strip()

        return IMDBData(
            rating=rating,
            votes=nr_votes,
            duration=duration,
            id=imdb_id
        )


print(IMDBScreaper().get_imdb_id("Thor"))