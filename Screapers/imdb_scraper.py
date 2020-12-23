import regex as re

from Screapers.helpers import get_html_from_url

class IMDBScreaper():
    def __init__(self):
        self.base_link = "https://www.imdb.com"
        self.movies = []

    def get_query_link(self, movie_name):
        return f"{self.base_link}/find?q={movie_name}"

    def check_good_header(self,header_div):
        header_name = header_div.find("h3", {"class": "findSectionHeader"}).get_text()
        return header_name == "Titles"

    def query_name(self,movie_name:str):
        return movie_name.replace(" ","+")

    def get_first_link_result(self, movie_name):
        query_name = self.query_name(movie_name)
        query_link = self.get_query_link(query_name)
        html = get_html_from_url(query_link)

        all_headers = html.find_all("div", {"class": "findSection"})
        movie_heading = list(filter(lambda header_div : self.check_good_header(header_div), all_headers))
        if len(movie_heading) == 0:
            raise Exception(f"No movies found on {self.base_link} with the name '{movie_name}'")
        movie_heading = movie_heading[0]

        result = movie_heading.find("td", {"class": "result_text"}) # get the first movie restul
        movie_link = result.find('a')['href']
        return self.base_link + movie_link

    def run_scraper(self, movie_name) -> dict:
        movie_link = self.get_first_link_result(movie_name)
        print(movie_link)
        html = get_html_from_url(movie_link)
        imdb_id = re.findall("\d+", movie_link)[0]

        rating_class = html.find("div", {"class": "imdbRating"})
        rating = rating_class.find("strong").get_text()
        nr_votes = rating_class.find("span", {"class": "small"}).get_text()

        subtext = html.find("div", {"class": "subtext"})
        duration = subtext.find("time").get_text().strip()

        movie = {
            "rating": rating,
            "number_votes": nr_votes,
            "duration": duration,
            "imdb_id": imdb_id,
        }
        return movie
