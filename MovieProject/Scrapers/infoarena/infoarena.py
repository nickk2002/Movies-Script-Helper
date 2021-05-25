import pandas as pd
import requests
from bs4 import BeautifulSoup

def returneaza_informatii(t_row):
    id = t_row.find("td", class_="number")
    problema = t_row.find("td", class_="task")
    autor = t_row.find("td", class_="author")
    sursa = t_row.find("td", class_="source")
    nrCompetitori = t_row.find("td", class_="")

    dictionar = {
        "id": id.text,
        "problema": problema.text,
        "autor": autor.text,
        "sura": sursa.text,
        "nrCompetitori": int(nrCompetitori.text)
    }

    return dictionar

dfObj = pd.DataFrame()
list_dictionaries = []
for i in range(0, 250, 250):
    infoarena_url = f"https://www.infoarena.ro/arhiva?display_entries=250&first_entry={i}"
    get_request = requests.get(infoarena_url)
    general_soup = BeautifulSoup(get_request.content, "lxml")
    table_problems = general_soup.find("table", class_="tasks sortable")
    table_rows = table_problems.find_all("tr")
    #print(t_rows)

    for id, t_row in enumerate(table_rows[1:]):
        dict = returneaza_informatii(t_row)
        list_dictionaries.append(dict)

print(list_dictionaries)
# dfObj = pd.DataFrame(list_dictionaries)
# dfObj.to_excel("lista_infoarena_prbleme.xlsx")