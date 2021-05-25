import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Scrapers.MyScraperLibrary.email_sender import send_message
from Scrapers.helpers import wait_to_load
from Scrapers.settings import Selenium


class VaccinScraper:
    user = "n_filat@yahoo.com"
    password = "Niculin@2021"
    login_url = "https://programare.vaccinare-covid.gov.ro/auth/login"
    base_url = 'https://programare.vaccinare-covid.gov.ro/#/appointment/new/2906458'
    submit_delay = 3

    def __init__(self):
        chrome_options = ChromeOptions()
        chrome_options.headless = True
        self.browser = webdriver.Chrome(
            executable_path=Selenium.CHROME_DRIVER_PATH,
            options=chrome_options)

        self.browser.maximize_window()
        self.logged_in = False

    def scrape(self, judet_name):
        if not self.logged_in:
            self.browser.get(self.login_url)
            self.login(self.user, self.password)
            print(self.browser.current_url)
            wait_to_load(self.browser, By.ID, 'home', wait_time=10)
            self.browser.get(self.base_url)
        lista = self.check(judet_name)
        return lista

    @staticmethod
    def get_info(row):
        soup = BeautifulSoup(row.get_attribute('innerHTML'), 'lxml')
        mat_cells = soup.find_all('mat-cell')
        name = mat_cells[0].text.strip()
        address = mat_cells[3].text.strip()
        locuri = soup.find('mat-chip').text.strip()
        select_button = row.find_element_by_xpath('.//button')

        return {
            'name': name,
            'address': address,
            'locuri': locuri,
            'select': select_button,
        }

    @staticmethod
    def check_for_available_stuff(rows):
        scraped_data = [VaccinScraper.get_info(row) for row in rows]
        filtered_list = [data for data in scraped_data if data['locuri'] != '0']
        if filtered_list:
            return filtered_list
        return None

    def login(self, username, password):
        user_field = wait_to_load(self.browser, By.NAME, "username")
        user_field.send_keys(username)

        password_field = wait_to_load(self.browser, By.NAME, "password")
        password_field.send_keys(password)

        login_button = wait_to_load(self.browser,
                                    By.XPATH,
                                    "//*[@id='mat-tab-content-0-0']/div/app-authenticate-with-email/form/button", 10)
        login_button.click()
        print("logged in!")
        self.logged_in = True

    def more_items_on_page(self):
        switch_to_more_on_page = wait_to_load(self.browser, By.XPATH, '//*[@id="mat-select-0"]/div')
        switch_to_more_on_page.click()

        switch_to_more_on_page = wait_to_load(self.browser, By.XPATH, '//*[@id="mat-option-3"]')
        switch_to_more_on_page.click()

    def filter_rows(self, judet_name: str):
        judet = wait_to_load(self.browser, By.XPATH, '//*[@id="mat-input-2"]', wait_time=10)
        judet.clear()
        judet.send_keys(judet_name)

        judet.send_keys(Keys.DOWN)
        judet.send_keys(Keys.ENTER)

        filtreaza = wait_to_load(self.browser, By.XPATH, '//*[@id="cdk-accordion-child-0"]/div/div/div/button[1]')
        filtreaza.send_keys(Keys.ENTER)
        print("Am dat filter")
        print("Zooming out")
        self.browser.execute_script("document.body.style.zoom='60%'")
        print("Start sleeping for", self.submit_delay, "seconds")
        time.sleep(self.submit_delay)
        print("end sleeping")

    def check(self, judet_name):
        self.filter_rows(judet_name)
        rows = self.browser.find_elements_by_xpath('//mat-row')
        return self.check_for_available_stuff(rows)


city_name = "Bucuresti"
scraper = VaccinScraper()
scraped_data = scraper.scrape(city_name)

test_list = [
    {'name': 'SALA DE SPORT A MUNICIPALITATII', 'address': 'BAIA DE ARAMA , STR. STADIONULUI , NR.7', 'locuri': '621'},
    {'name': 'SALA DE SPORT A MUNICIPALITATII', 'address': 'STREHAIA , STR. MATEI BASARAB , NR. 22', 'locuri': '83'},
    {'name': '', 'adress': '', 'locuri': ''},
    {'name': '', 'adress': '', 'locuri': ''}]

message = f'''Am gasit o optiune pentru a te programa la vaccin mami.Optiunea este pentru {city_name} Daca primesti acest email script-ul functioneaza!
Sa incerci sa te grabesti si sa intrii in aplicatie ca sa poti sa te programezi.
Aici e linkul de logat : {VaccinScraper.login_url}

Optiunile pe care le ai:
'''
retry_interval = 60 * 30  # 30 minutes
attempts = 0
while True:
    if scraped_data:
        print("Am gasit pt", city_name)

        for index, element in enumerate(scraped_data):
            row_message = f'{index}. {element["name"]} la adresa {element["address"]} Are {element["locuri"]} locuri libere'
            message += row_message
            message += '\n'
        send_message(message, to_self=True)
        send_message(message, destinatator='n_filat@yahoo.com')
        scraper.browser.quit()
        break
    else:
        attempts += 1
        print(f"Attempt {attempts}. Nu am gasit momentan nimic pentru {city_name}.Incercam din nou!", )
        print("Sleeping for", retry_interval / 60, "minutes")
        time.sleep(retry_interval)
        scraper.scrape(city_name)
