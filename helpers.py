from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait


def wait_to_load(browser, search_type, input, wait_time = 1):
    return Wait(browser, wait_time).until(
        EC.visibility_of_element_located((search_type, input)))

def get_html_from_url(url):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(request).read().decode("utf-8")
    return BeautifulSoup(html,'html.parser')
