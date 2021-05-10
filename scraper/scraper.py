from bs4 import BeautifulSoup
from typing import *
from time import sleep
import requests
import random
import json


YEAR = 2021
PREFIX = "https://basketball-reference.com"


def get_soup(url: str):
    sleep(random.choice([0.1, 0.25, 0.5]))
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')


def get_team_urls(url: str) -> Set[Tuple[str, str]]:
    soup = get_soup(url)
    table = soup.find_all("tr", class_="full_table")
    team_urls = set()
    for row in table:
        team_urls.add((row.find("a").get_text(), row.find("a")["href"]))
    return team_urls


def get_table(soup):
    table = soup.find(id="div_roster")
    return table.find_all("tr")


def set_roster(table, team_name, year, data):
    roster = []
    for player_row in table[1:]:
        columns = player_row.find_all("td")
        player = {}
        for col in columns:
            if col["data-stat"] == "player":
                name = col.get_text()
                slug = col.find("a")["href"].split('/')[-1].split(".")[0]
                player["slug"] = slug
                if name[-6:].strip() == "(TW)":
                    name = name[:-6]
                player["name"] = name
            elif col["data-stat"] == "birth_date":
                player["dob"] = col.get_text()
        roster.append(player)

    data[year].append({"team": team_name, "roster": roster})


if __name__ == "__main__":
    data = {}
    while YEAR >= 1950:
        team_urls = get_team_urls(
            f'https://www.basketball-reference.com/leagues/NBA_{YEAR}.html')
        data[YEAR] = []
        for team_name, url in team_urls:
            full_team_url = PREFIX + url
            table_roster = get_table(get_soup(full_team_url))
            print(team_name, YEAR)
            set_roster(table_roster, team_name, YEAR, data)
        YEAR -= 1
    with open('../data.json', 'w') as outfile:
        json.dump(data, outfile)
