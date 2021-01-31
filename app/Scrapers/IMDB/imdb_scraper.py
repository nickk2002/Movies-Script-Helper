import concurrent
import enum
import time
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass

import pandas as pd
import regex as re
from bs4 import BeautifulSoup

from Scrapers.MyScraperLibrary.ScraperQuery import ScaperQuery


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
    duration: int  # in minutes
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


def load_as_string(ls: list):
    return "".join(str(ls))


class IMDBScraper(ScaperQuery):
    base_link = "https://www.imdb.com"

    # use_proxy = True

    # use_scraperapi = True

    def get_query_link(self, query_name):
        return f"/find?q={query_name}&s=tt&ref_=fn_tt_ex&exact=true&ttype=ft"

    @staticmethod
    def parse_number(number):
        try:
            number = re.findall("\d+", number)[0]
            return int(number)
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

    @staticmethod
    def get_imdb_id(url) -> int:
        imdb_id = re.findall('\d+', url)[0]
        return imdb_id

    def get_imdb_id_duration(self, url, soup: BeautifulSoup):
        imdb_id = self.parse_number(url)
        result = str(soup.select('div.txt-block>time'))
        duration = int(self.parse_number(result))
        return imdb_id, duration

    def parse_integer(self, integer: str):
        # the integer might have commas and we have to replace them
        integer = integer.replace(',', '')
        return self.parse_number(integer)

    @staticmethod
    def get_year(soup: BeautifulSoup):
        year_span = soup.find("span", id="titleYear")
        if year_span:
            return year_span.a.get_text()  # get the year url, then get the actual text
        return None

    @staticmethod
    def get_release_day(soup: BeautifulSoup):
        # release day
        release_day_soup = soup.find('a', title="See more release dates")
        release_day = release_day_soup.get_text()  # Release Day 6 May 2011 (Romania)
        # remove the parens
        release_day = release_day[0:release_day.find('(')].strip()  # Release Day 6 May 2011
        return release_day

    def get_general_movie_data(self, soup: BeautifulSoup):
        general_movie_elements = soup.find_all(class_="credit_summary_item")
        general_movie_data = {}
        for person_soup in general_movie_elements:
            actual_text = person_soup.get_text().strip().replace('\n', ' ')
            person_url = person_soup.a['href']
            person_id = int(self.parse_number(person_url))
            field_name, values = actual_text.split(':')
            if not field_name.endswith('s'):
                field_name += 's'
            values = [(name.strip(), person_id) for name in values.split(',')]
            general_movie_data[field_name] = values
        return general_movie_data

    def parse_scraped_data(self, scraped_data: dict):
        """
            returns a dict to excel, joining lists to strings
        """
        for (key, value) in scraped_data.items():
            if type(value) is list:
                try:
                    parsed_string = " | ".join(value)
                    scraped_data[key] = parsed_string
                except TypeError:
                    continue
        return scraped_data

    def full_scrape(self, url, soup: BeautifulSoup):
        error_404 = soup.find(class_="error_code_404")
        if error_404:
            raise IMDB404Error("There is no movie at the url", url)
        imdb_id = self.parse_number(url)  # get imdb_id from url
        print("ID:", imdb_id)

        year = self.get_year(soup)
        release_day = self.get_release_day(soup)
        if soup.find(text=re.compile("too fast")):
            raise Exception("Too fast requests warning")
        name = soup.find("div", class_="title_wrapper").h1.text
        print("Title:", name)

        plot_summary = soup.find(class_="plot_summary")
        description = plot_summary.find(class_="summary_text").get_text().strip()
        if description == "Add a Plot »":
            description = "No description."

        # get director|writers|stars|
        general_movie_data = self.get_general_movie_data(soup)

        # rating stuff
        rating_class = soup.find(class_="imdbRating")

        if rating_class:
            rating = rating_class.find("strong").get_text()
            nr_votes = rating_class.find("span", class_="small").get_text()
            if nr_votes:
                nr_votes = self.parse_integer(nr_votes)
        else:
            rating = nr_votes = 0

        # cast list
        cast_list = soup.find(class_="cast_list")
        cast = []
        if cast_list:
            cast_rows = cast_list.find_all(class_=re.compile("odd|even"))
            for cast_row in cast_rows:
                # get the star name + id
                star_part = cast_row.find("td", class_="").a
                url = star_part['href']
                star_name = star_part.get_text().strip()
                star_id = self.parse_number(url)

                # get the character name + id
                character_part = cast_row.find(class_="character").a
                if character_part:
                    url = character_part['href']
                    character_name = character_part.get_text().strip()
                    character_id = self.parse_number(url)
                else:
                    character_name = character_id = None
                cast.append(
                    {
                        "star": star_name,
                        "star_id": star_id,
                        "character": character_name,
                        "character_id": character_id,
                    }
                )

        subtext_info = soup.find(class_="subtext")
        genre_list = [url.get_text() for url in subtext_info.find_all("a") if url.get("href").startswith("/search")]

        movie_details = soup.find(id="titleDetails").find_all(class_="txt-block")
        info_values = {}
        for detail in movie_details:
            detail_text = detail.get_text().strip()
            if len(detail_text.split(":")) == 2:
                key, value = detail_text.split(":")
                if "See more" in value:
                    index = value.find("See more")
                    value = value[0: index]
                value = value.strip().replace('\n', ' ')
                parsed_value = value

                if "$" in value or "€" in value:
                    parsed_value = self.parse_integer(value)
                else:
                    splitted_values = re.split('[|,]', value)
                    if len(splitted_values) > 1:
                        parsed_value = [_.strip() for _ in splitted_values]
                info_values[key] = parsed_value
        # print(json.dumps(info_values, indent=4))
        country = info_values.get('Country')
        budget = info_values.get('Budget')
        total_gross = info_values.get("Cumulative Worldwide Gross")
        language = info_values.get('Language')
        filming_locations = info_values.get('Filming Locations')
        result = str(soup.select('div.txt-block>time'))
        duration = self.parse_number(result)

        information = {
            "id": imdb_id,
            "year": year,
            "name": name,
            "rating": rating,
            "votes": nr_votes,
            "description": description,
            "genres": genre_list,
            "stars": general_movie_data.get("Stars"),
            "writes": general_movie_data.get("Writers"),
            "cast": cast,
            "directors": general_movie_data.get("Directors"),
            "release_day": release_day,
            "country": country,
            "language": language,
            "filming_locations": filming_locations,
            "budget": budget,
            "total_gross": total_gross,
            "duration": duration,
        }
        return self.parse_scraped_data(information)
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


def scraping_threading(start_index, end_index):
    scraper = IMDBScraper()
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_data = [executor.submit(scraper.get_information, imdb_id) for imdb_id in range(start_index, end_index)]
        scraped_data = []
        start_time = time.time()
        for future in concurrent.futures.as_completed(future_data):
            try:
                data = future.result()
                scraped_data.append(data)
            except IMDB404Error:
                continue
        print("For scraping", end_index - start_index + 1, "pages it took", time.time() - start_time, "seconds")
    return scraped_data


if __name__ == "__main__":

    #     # information = []
    #         # information.append(scraper.get_information(i))

    file_name = 'imdb_data.csv'
    increment = 200
    start_id = 1400
    for i in range(start_id, start_id + increment * 2, increment):
        information = list(scraping_threading(i, i + 200))
        df = pd.DataFrame(information)
        df.to_csv(file_name, mode='a', encoding='utf-8', header=False)
        print(f"Written to {file_name} {increment} movie entries")
