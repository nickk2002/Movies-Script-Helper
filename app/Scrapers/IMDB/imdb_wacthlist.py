import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from Scrapers.helpers import wait_to_load

from Scrapers.settings import Selenium

base_url = "https://www.imdb.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.imdb.com%2Fregistration%2Fap-signin-handler%2Fimdb_us&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=imdb_us&openid.mode=checkid_setup&siteState=eyJvcGVuaWQuYXNzb2NfaGFuZGxlIjoiaW1kYl91cyIsInJlZGlyZWN0VG8iOiJodHRwczovL3d3dy5pbWRiLmNvbS9yZWdpc3RyYXRpb24vY29uZmlybWF0aW9uP3JlZl89bG9naW4ifQ&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path=Selenium.CHROME_DRIVER_PATH,options=options)
driver.get(base_url)

user = "mihai.filat@yahoo.com"
password = "tankionline"

time.sleep(1)
driver.find_element_by_name("email").send_keys(user)
time.sleep(1)
driver.find_element_by_name("password").send_keys(password)
time.sleep(1)
driver.find_element_by_id("signInSubmit").click()

time.sleep(1)
driver.get("https://www.imdb.com/user/ur79162207/watchlist")
wait_to_load(driver,By.CLASS_NAME,"lister-details")

print(driver.current_url)

titles = driver.find_element_by_css_selector("body")

body = titles.find_element_by_class_name("pagecontent")
with open("watchlist.html","w",encoding='ansi') as f:
    f.write(body)
soup = BeautifulSoup(body,"html.parser")