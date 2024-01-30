from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

url_linie = 'https://www.bazakolejowa.pl/_fervojoj/LINIE/LINIE.HTM'

response_linie = requests.get(url_linie)
html_content_linie = response_linie.content

soup_linie = BeautifulSoup(html_content_linie, 'html.parser')

links_to_trasy = soup_linie.find_all('a', href=True)
trasy = []
i = 0

for link in links_to_trasy:
    trasa_url = urljoin(url_linie, link['href'])
    response_trasa = requests.get(trasa_url)
    html_content_trasa = response_trasa.content
    trasy.append([])
    soup_trasa = BeautifulSoup(html_content_trasa, 'html.parser')

    frame_src = soup_trasa.find('frame', {'src': 'SPIS.HTM'})

    if frame_src:
        frame_url = frame_src['src']

        target_url = urljoin(trasa_url, frame_url)

        response_target = requests.get(target_url)
        html_content_target = response_target.content

        soup_target = BeautifulSoup(html_content_target, 'html.parser')

        links_to_stations = soup_target.select('body a[href$=".HTM"]')
        with open('wyniki.txt', 'a', encoding='utf-8') as file:
            for idx, station_link in enumerate(links_to_stations[1:-2], start=1):
                station_name = station_link.get_text(strip=True)
                trasy[i].append(station_name)
                # print(f"Trasa: {link.get_text(strip=True)}, Stacja: {station_name}")
            file.write(str(trasy[i])+'\n')
    else:
        break
    print(trasy[i])
    i += 1
