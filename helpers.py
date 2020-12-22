from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def get_html_from_url(url):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(request).read().decode("utf-8")
    return BeautifulSoup(html,'html.parser')
