import requests
from bs4 import BeautifulSoup
import json


if __name__ == "__main__":
    r = requests.get('https://www.immobiliare.it/affitto-case/napoli/?criterio=rilevanza&prezzoMassimo=600&idMZona[]=78&idMZona[]=10323&idMZona[]=79&idQuartiere[]=283&idQuartiere[]=12816&idQuartiere[]=12815&idQuartiere[]=273&idQuartiere[]=261&idQuartiere[]=12814&idQuartiere[]=12826&idQuartiere[]=12824')
    soup = BeautifulSoup(r.content, 'html.parser')
    results = soup.find("ul", {"data-cy": "result-list"})
    children = results.findChildren("li", recursive=False)
    with open("results.json", "r", encoding="UTF8") as j:
        content = j.read()

    with open("results.json", "w", encoding="UTF8") as j:
        old_list = json.loads(content)
        print("old\n", len(old_list))
        current_list = []
        for r in children:
            try:
                title = r.find("a", {"class": "in-card__title"})
                link = r.find("a")["href"]
                # print(title.text, link)
                current_list.append({"title": title.text, "link": link})
            except Exception:
                pass
        print("new\n", len(current_list))
        json_list = json.dumps(current_list, indent=4)
        j.write(json_list)

    if len(old_list) != len(current_list):
        new_elements = set(current_list) - set(old_list)
        for x in list(new_elements):
            print(x)
