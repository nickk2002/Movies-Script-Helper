import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from Scrapers.MyScraperLibrary.ScraperQuery import ScaperQuery
from Scrapers.helpers import wait_to_load
from Scrapers.settings import Selenium
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import json
import requests
from scraper_api import ScraperAPIClient
import seleniumrequests

class VaccinScraper(ScaperQuery):
    base_link = "https://programare.vaccinare-covid.gov.ro/#/home"
    login = True
    user = "n_filat@yahoo.com"
    password = "Niculin@2021"
    login_url = "https://programare.vaccinare-covid.gov.ro/auth/login"

    def __init__(self):
        super().__init__()
        chrome_options = ChromeOptions()
        chrome_options.headless = True
        self.browser = seleniumrequests.Chrome(
            executable_path=Selenium.CHROME_DRIVER_PATH,
            options = chrome_options)


    def login_requests(self, user, password):
        self.session.get(self.base_link)  # first get the base link

        data = {"username": user, "password": password}
        data[
            "captcha-challenge"] = "03AGdBq24s_O85C622XXl1ggAApqwK1KdWQRCQMY0c6YadpCC55sUhLssxqoee161X3xpei2jbrE1fyJtsVdzJeAenpBajJuILh7H9E8bADFXpsBl7KxHsnvL8Qa9fwxI8fCQi1oarScQLduP5FALEnU6SQhU_bvIaFf3dMeu0rlPfrowPZzR1p4mVADsk5BmOHUJkgKGdGuxcNUtfQ90AAHSF77_k606kJAkuU-7_dJCj9H1DKnHlimyiQBFq6aDJIO5yzShuqp8jZdulqyicRzgVXPd5yIr0LcLA81ohdfdvLdk9dJQR2K-Q3KHU6I6IHZvewGBkudVpaVUUbP3OPU6I6wohuSOkT97Z5FehRtmgZPZ1qY64o6FO1e2Rid5HlJqu7qFrCAYMXT505FMeYf6AtNk3jzo4gLOOLWMXZZkE1mtEZCzaAEa3pCmHnMw8Y2h5cB_jWBVShiM1oCbvt_W1XFCqA8Z784au1Ja6ZOlz8MpB0QGh4FWZaufrjXUfy49byyMsN66djNPN4YtNP64zFIyDHrRpjjubH7rnQWePtpZJF2ESYLo"

        soup = self.get_soup_from_url(self.base_link)
        login_action_url = self.login_url

        self.session.post(login_action_url, data=data, headers=self.headers)

        # check if the login was ok, this should be implemented by the user
        self.check_good_login(
            soup=self.get_soup_from_url(self.base_link),
            data=data)  # will raise exception if the login failed
        print(data)

    def login_selenium(self):
        self.browser.get(self.login_url)
        user = wait_to_load(self.browser, By.NAME, "username")
        user.send_keys(self.user)

        user = wait_to_load(self.browser, By.NAME, "password")
        user.send_keys(self.password)

        login_button = wait_to_load(self.browser,
                                    By.XPATH,
                                    "//*[@id='mat-tab-content-0-0']/div/app-authenticate-with-email/form/button", 10)
        login_button.click()

    def check_good_login(self, soup: BeautifulSoup, data):
        soup = self.get_soup_from_url("https://programare.vaccinare-covid.gov.ro/#/recipients")
        print(soup)

    def login_scraper_api(self):
        client = ScraperAPIClient("827a189a13edb3490a8ea907a6f61d47")
        print("HERE")
        data = {"username": self.user, "password": self.password}
        r = client.get(url=self.login_url)
        print(r.text)
    def run(self):
        # self.login_requests(user=self.user, password=self.password)
        self.login_selenium()

        print("logged in")

        # judet = wait_to_load(self.broswer,By.XPATH,"//*[@id='mat-input-2']")
        # judet.send_keys("Bucuresti")
        #
        # filtreaza = wait_to_load(self.broswer,By.XPATH,'//*[@id="cdk-accordion-child-0"]/div/div/div/button[1]')
        # filtreaza.click()
        self.session = requests.session()
        self.session.headers = {}

        for cookie in self.browser.get_cookies():
            c = {cookie['name']: cookie['value']}
            self.session.cookies.update(c)


        print(self.session.headers)
        print(self.session.cookies)
        print('==========')

        payload = {"countyID": 40, "localityID": "null", "name": "null"}
        headers = {
            "user-agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        }
        r = requests.get("https://programare.vaccinare-covid.gov.ro/auth/login",headers)
        print(r.content)
        #
        # r = self.session.post(,data=payload)
        # print(r.status_code)
        # print(r.content)
        # print(r.json())
