import concurrent
import time
from concurrent.futures.thread import ThreadPoolExecutor

import pandas as pd
import regex as re
from bs4 import BeautifulSoup

from MovieProject.Scrapers.MyScraperLibrary.ScraperQuery import ScaperQuery
from MovieProject.Scrapers.helpers import append_df_to_excel
from .exceptions import IMDB404Error, IMDBNoMoviesFound
from .imdb_data import IMDBData
from .scrape_mode import IMDBScrapeMode


def load_as_string(ls: list):
    return "".join(str(ls))


class IMDBScraper(ScaperQuery):
    base_link = "https://www.imdb.com"

    # use_proxy = True

    # use_scraperapi = True
    # proxies = ["51.158.68.133:8811"]

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
        if result is None:
            result = str(soup.select("div.subtext>time"))
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
        if release_day_soup is None:
            return None
        release_day = release_day_soup.get_text()  # Release Day 6 May 2011 (Romania)
        # remove the parens
        release_day = release_day[0:release_day.find('(')].strip()  # Release Day 6 May 2011
        return release_day

    def get_movie_duration(self, soup: BeautifulSoup):
        result = soup.select_one('div.txt-block>time')
        if result is None:
            result = soup.select_one("div.subtext>time")
        if result is None:
            return None
        result = result.text.strip()
        duration = int(self.parse_number(result))
        return duration

    def get_general_movie_data(self, soup: BeautifulSoup):
        general_movie_elements = soup.find_all(class_="credit_summary_item")
        general_movie_data = {}
        for person_soup in general_movie_elements:
            actual_text = person_soup.get_text().strip().replace('\n', ' ')
            person_url = person_soup.a['href']
            person_id = int(self.parse_number(person_url))
            split_pos = actual_text.find(':')
            field_name = actual_text[:split_pos]
            values = actual_text[split_pos + 1:]
            if not field_name.endswith('s'):
                field_name += 's'

            def remove_see_full_cast_from_name(name):
                pattern = "| See full cast"
                if pattern in name:
                    return name[0: name.find(pattern)]
                return name

            values = [(remove_see_full_cast_from_name(name.strip()), person_id) for name in values.split(',')]

            # values = map(remove_see_full_cast_from_name,values)
            general_movie_data[field_name] = values
        print(general_movie_data)
        return general_movie_data

    @staticmethod
    def parse_scraped_data(scraped_data: dict):
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

    def check_if_movie_exists(self, url, soup: BeautifulSoup):
        error_404 = soup.find(class_="error_code_404")
        if error_404:
            raise IMDB404Error("There is no movie at the url", url)
        return True

    def full_scrape(self, url, soup: BeautifulSoup):
        # if soup.find(text=re.compile("too fast")):
        #     raise Exception("Too fast requests warning", soup)
        self.check_if_movie_exists(url, soup)

        imdb_id = self.parse_number(url)  # get imdb_id from url
        print("ID:", imdb_id)

        year = self.get_year(soup)
        release_day = self.get_release_day(soup)

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
                if not star_part:
                    # we have a row that does not have any link
                    continue
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
        duration = self.get_movie_duration(soup)

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
        return information
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

    @staticmethod
    def parse_number_to_id(number):
        imdb_id = str(number)
        if imdb_id.startswith("tt"):
            imdb_id = imdb_id[2:]
        if len(imdb_id) < 7:
            imdb_id = "0" * (7 - len(imdb_id)) + imdb_id
        return imdb_id

    def get_information(self, imdb_id, scrape_mode: IMDBScrapeMode):
        imdb_id = self.parse_number_to_id(imdb_id)
        page_url = f"https://www.imdb.com/title/tt{imdb_id}/?ref_=fn_al_tt_1"
        soup = self.get_soup_from_url(page_url)
        if scrape_mode == IMDBScrapeMode.FullScrape:
            return self.full_scrape(page_url, soup)
        elif scrape_mode == IMDBScrapeMode.CHECK_EXISTS:
            return self.check_if_movie_exists(page_url, soup)


def scraping_threading(start_index, end_index):
    scraper = IMDBScraper()
    with ThreadPoolExecutor(max_workers=100) as executor:
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


def scrape_normal():
    scraper = IMDBScraper()
    scraped_data = []
    start_time = time.time()

    file_name = 'imdb_data.xlsx'

    df = pd.read_excel(file_name, engine='openpyxl')
    ids = df['id'].values.sort()
    last_id = int(ids[len(ids) - 1])
    for id in range(last_id, 100000):
        try:
            data = scraper.get_information(id)
            scraped_data.append(data)
        except IMDB404Error:
            continue
    # print("For scraping", end_index - start_index + 1, "pages it took", time.time() - start_time, "seconds")
    return scraped_data


def scrape_to_excel():
    file_name = 'imdb_data.xlsx'

    df = pd.read_excel(file_name, engine='openpyxl')
    ids = sorted(df['id'].values)
    last_id = int(ids[len(ids) - 1])
    start_id = last_id + 1
    print("last id is", last_id)
    start_time = time.time()
    increment = 500
    for i in range(start_id, start_id + increment * 100, increment):
        information = list(scraping_threading(i, i + increment))
        # sorted_information = sorted(information,key = lambda data : data['id'])
        df = pd.DataFrame(information)
        append_df_to_excel(file_name, df, header=False, index=False)
        print("putting data to excel")
        print("Actual time from the start of the script is", time.time() - start_time, "scraped:", i - start_id)


def debug_id(id):
    scraper = IMDBScraper()
    info = scraper.get_information(id)


if __name__ == "__main__":
    # debug_id(6468322)
    print("Oh no!")
    scrape_to_excel()
    # print(info)
    # df = pd.DataFrame([info])
    # append_df_to_excel('imdb_data.xlsx',df,header=False,index=False)
