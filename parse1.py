import requests
from bs4 import BeautifulSoup
import json


url = 'https://www.sports.ru/hockey/tournament/nhl/bombardiers/'
response = requests.get(url)

# Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

release_links = []

for link in soup.find_all('td', class_ = 'name-td alLeft bordR'):
    
    link_p=link.find_parent('tr')

    N = link_p.find_all('td')[0].text.strip()
    name = link_p.find_all('td')[1].text.strip()
    team = link_p.find_all('td')[2].text.strip()
    games =link_p.find_all('td')[3].text.strip()
    goals =link_p.find_all('td')[4].text.strip()
    assists =link_p.find_all('td')[5].text.strip()
    points = link_p.find_all('td')[6].text.strip()
    

    release_links.append({
                "№": N,
                "Имя": name,
                "Команда": team,
                "Игр": games,
                "Голов": goals,
                "Передач": assists,
                "Очков": points,          
            })



print(release_links)

with open("Parsing1.json", "w", encoding='utf-8') as f:
        json.dump(release_links, f, indent=4, ensure_ascii=False)