import enum
from dataclasses import dataclass

import regex as re
from bs4 import BeautifulSoup

from Scrapers.MyScraperLibrary.ScraperQuery import ScaperQuery,ScraperMode


class IMDBScrapeMode(enum.Enum):
    FullScrape = 1
    ID = 2
    ID_DURATION = 3

@dataclass
class IMDBData:
    name: str
    id: str
    year: int
    director: str
    director_id: int
    release_day: str
    stars: list
    rating: float
    duration: int  # in mimutes
    votes: int
    genres: list
    description: str
    cast: list
    budget: int

    def __str__(self):
        output = self.__class__.__name__ + "(\n"
        for (cnt, (key, value)) in enumerate(self.__dict__.items()):
            output += f'{key}={value.__str__()}'
            if cnt != len(self.__dict__.items()) - 1:
                output += ",\n"
        output += ")"
        return output


class IMDB404Error(Exception):
    pass


class IMDBNoMoviesFound(Exception):
    pass


class IMDBScreaper(ScaperQuery):
    base_link = "https://www.imdb.com"

    def get_query_link(self, query_name):
        return f"/find?q={query_name}&s=tt&ref_=fn_tt_ex&exact=true&ttype=ft"

    @staticmethod
    def parse_number(number):
        try:
            number = re.findall("\d+", number)[0]
            return number
        except IndexError:
            Exception("regex could not find an integer match for string", number)
            return None

    @staticmethod
    def check_good_header(header_div):
        header_name = header_div.find("h3", class_="findSectionHeader").get_text()
        return header_name == "Titles"

    def handle_query_result(self, query_url: str, soup: BeautifulSoup, scrape_enum):
        find_message = soup.find('h1', class_="findHeader").get_text()
        if find_message.startswith("No results"):
            raise IMDBNoMoviesFound(f"No movies found on {self.base_link} with the name '{self.query_name}'")

        # get the first result that matches the query
        result = soup.find("td", class_="result_text")
        movie_link = result.a['href']
        print(f"scraping imdb using {scrape_enum} mode.")

        if scrape_enum == IMDBScrapeMode.FullScrape:
            return self.get_url(url=movie_link, callback=self.full_scrape)
        elif scrape_enum == IMDBScrapeMode.ID:
            return self.get_imdb_id(url=movie_link)
        elif scrape_enum == IMDBScrapeMode.ID_DURATION:
            return self.get_url(url=movie_link, callback=self.get_imdb_id_duration)

    def load_as_string(self, ls: list):
        return "".join(str(ls))

    def get_imdb_id(self, url) -> int:
        imdb_id = self.parse_number(url)
        return imdb_id
    def get_imdb_id_duration(self, url, soup : BeautifulSoup):
        imdb_id = self.parse_number(url)
        result = str(soup.select('div.txt-block>time'))
        duration = int(self.parse_number(result))
        return imdb_id,duration
    def full_scrape(self, url, soup: BeautifulSoup):
        error_404 = soup.find(class_="error_code_404")
        if error_404:
            raise IMDB404Error("There is no movie at the url", url)
        imdb_id = self.parse_number(url)  # get imdb_id from url
        year_span = soup.find("span", id="titleYear")
        year = year_span.a.get_text()  # get the year url, then get the actual text

        print("Year", year)

        # release day
        release_day_soup = soup.find('a', title="See more release dates")
        release_day = release_day_soup.get_text()  # Release Day 6 May 2011 (Romania)
        # remove the parens
        release_day = release_day[0:release_day.find('(')].strip()  # Release Day 6 May 2011

        print("Release Day", release_day)

        plot_summary = soup.find(class_="plot_summary")
        description = plot_summary.find(class_="summary_text").get_text().strip()
        if description == "Add a Plot »":
            description = "No description."

        # get director|writers|stars|
        director_writers_stars = soup.find_all(class_="credit_summary_item")
        director_line = writers_line = stars_line = None
        for header_soup in director_writers_stars:
            actual_text = header_soup.get_text().strip()
            if actual_text.startswith("Director:"):
                director_line = header_soup
            if actual_text.startswith("Writers"):
                writers_line = header_soup
            if actual_text.startswith("Stars"):
                stars_line = header_soup

        # get the director
        if director_line:
            director_url = director_line.a['href']
            director_id = self.parse_number(director_url)
            director_name = director_line.a.get_text()
        print("director ", director_name, director_id)

        # get the movie stars
        stars = []
        if stars_line:
            for star_soup in stars_line.find_all('a'):
                url = star_soup['href']
                if url.startswith("/name"):
                    star_name = star_soup.get_text()
                    star_id = self.parse_number(url)
                    stars.append((star_name, star_id))
        print("stars ", stars)

        # cast list
        cast_list = soup.find(class_="cast_list")
        cast_rows = cast_list.find_all(class_=re.compile("odd|even"))
        cast = []

        for cast_row in cast_rows:
            # get the star name + id
            star_part = cast_row.find("td", class_="").a
            url = star_part['href']
            star_name = star_part.get_text().strip()
            star_id = self.parse_number(url)

            # get the character name + id
            character_part = cast_row.find(class_="character").a
            url = character_part['href']
            character_name = character_part.get_text().strip()
            character_id = self.parse_number(url)
            cast.append((star_name, star_id, character_name, character_id))

        # rating stuff
        rating_class = soup.find(class_="imdbRating")

        if rating_class:
            rating = rating_class.find("strong").get_text()
            nr_votes = rating_class.find("span", class_="small").get_text()
            if nr_votes:
                nr_votes = nr_votes.replace(",", "")
                nr_votes = int(nr_votes)
        else:
            rating = nr_votes = 0

        subtext_info = soup.find(class_="subtext")
        genre_list = [url.get_text() for url in subtext_info.find_all("a") if url.get("href").startswith("/search")]

        if soup.find("div", class_="originalTitle"):
            name = soup.find(class_="originalTitle").get_text()
            name = name[0:name.find("(original title)")].strip()
        else:
            name = soup.find("div", class_="title_wrapper").h1.get_text()

        title_details = soup.find(id="titleDetails")
        movie_details = title_details.find_all(class_="txt-block")
        filter_names = ["Country", "Language", "Runtime", "Budget"]
        info_values = []
        for detail in movie_details:
            if detail.h4 is not None:
                detail_text = detail.get_text().strip()
                if len(detail_text.split(":")) == 2:
                    detail_name, value = detail_text.split(":")
                    value = value.strip().replace('\n', ' ')
                    if detail_name in filter_names:
                        info_values.append(value)
        country, language, budget, runtime = info_values
        budget = budget.replace(',', "")
        budget = self.parse_number(budget)
        duration = self.parse_number(runtime)
        print(duration, budget)
        genre_list = "|".join(genre_list)
        stars = "|".join([" ".join(star) for star in stars])
        cast = "|".join([" ".join(actor) for actor in cast])
        print("Genre:",genre_list)
        print("Stars:",stars)
        print("Cast:",cast)
        return {
            "id": imdb_id,
            "year": year,
            "name": name,
            "rating": rating,
            "votes": nr_votes,
            "description": description,
            "genres": genre_list,
            "stars": stars,
            "cast": cast,
            "director": director_name,
            "director_id": director_id,
            "release_day": release_day,
            "duration": duration,
            "budget": budget,
        }
        return IMDBData(
            id=imdb_id,
            name=name,
            rating=rating,
            votes=nr_votes,
            duration=duration,
            genres=genre_list,
            stars=stars,
            year=year,
            director=director_name,
            director_id=director_id,
            release_day=release_day,
            description=description,
            cast=cast,
            budget=budget,
        )

    def get_information(self, imdb_id):
        imdb_id = str(imdb_id)
        if imdb_id.startswith("tt"):
            imdb_id = imdb_id[2:]
        if len(imdb_id) < 7:
            imdb_id = "0" * (7 - len(imdb_id)) + imdb_id
        page_url = f"https://www.imdb.com/title/tt{imdb_id}/?ref_=fn_al_tt_1"
        soup = self.get_soup_from_url(page_url)
        return self.full_scrape(page_url, soup)


if __name__ == "__main__":
    scraper = IMDBScreaper()
    print(scraper.scrape("Thor", IMDBScrapeMode.ID))
