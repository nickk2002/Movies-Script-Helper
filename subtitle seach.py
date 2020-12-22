from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import regex as re
from selenium import webdriver
import time
import glob
import os
from rarfile import RarFile
RarFile.UNRAR_TOOL =r'C:\Program Files (x86)\UnrarDLL\UnRAR.dll'


driver = webdriver.Edge("C:\Windows\SystemApps\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\MicrosoftEdge.exe")
def download_subtitle(movie_name,path):

    global driver
    base_link = "https://www.imdb.com/find?q=" + movie_name
    request = Request(base_link, headers={'User-Agent': 'Mozilla/5.0'})
    file = urlopen(request)
    html = BeautifulSoup(file, 'html.parser')

    table = html.find_all("td", {"class": "result_text"})[0]
    movie_link = table.find_all('a')[0]['href']
    imdb_id = re.findall("\d+",movie_link)[0]

    print(imdb_id)

    driver.get("https://subs.ro/subtitrari/")
    python_button = driver.find_elements_by_xpath("//input[@type='submit']")[0]
    python_button.click()

    text = driver.find_elements_by_xpath("//input[@type='text' and @name='imdb']")[0]
    text.send_keys(imdb_id)
    time.sleep(0.1)
    python_button = driver.find_elements_by_xpath("//input[@type='submit' and @value='Caută']")[0]
    python_button.click()

    time.sleep(5)

    div = driver.find_elements_by_class_name("sub-buttons")[0]
    div.click()
    time.sleep(2)
    div = driver.find_elements_by_class_name("sub-buttons")[0]
    div.click()
    time.sleep(1)
    div = driver.find_elements_by_class_name("sub-buttons")[0]
    div.click()
    tot_href = driver.find_elements_by_xpath("//a[@class='btn-download']")[0]
    dw_link = tot_href.get_attribute('href')

    print(dw_link)

    list_of_files = glob.glob(r"M:\Quick Acces\Downloads")
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)



# def download(link,path):
#
#     path_creaza = path + os.sep + "subs"
#     if os.path.exists(path_creaza) == False:
#         os.mkdir(path_creaza)
#     r = R.get(link)
#     rar = Archive(r.content)
#     rar.extractall(path = path_creaza)



def yifi_all():
    lista = [file for file in os.scandir(dir) if file.is_dir() ]
    for file in lista:
        nume_lung = file.name
        path = file.path
        poz = nume_lung.find("(")
        nume = nume_lung
        if poz != -1:
            nume = nume_lung[:poz]
        download_subtitle(nume,path)

download_subtitle("jumanji","E:\Quick access\Desktop\Folder Test")
# download_subtitle("ready-player-one")
# download_subtitle("jumanji")