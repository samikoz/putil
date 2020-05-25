from bs4 import BeautifulSoup

import pathlib


def get_cached_daily_table():
    page_path: pathlib.Path = pathlib.Path('tests/resources/daily.html')
    table_id: str = 'main_table_countries'

    return BeautifulSoup(page_path.open('rb').read(), 'html.parser').find(id=table_id)


def get_cached_italy_table():
    page_path: pathlib.Path = pathlib.Path('tests/resources/italy.html')
    return BeautifulSoup(page_path.open('rb').read(), 'html.parser').find('table', {'class': 'wikitable'})


def get_cached_south_korea_table():
    page_path: pathlib.Path = pathlib.Path('tests/resources/south_korea.html')
    return BeautifulSoup(page_path.open('rb').read(), 'html.parser').find_all('table', {'class': 'wikitable'})[4]


def get_cached_france_table():
    page_path: pathlib.Path = pathlib.Path('tests/resources/france.html')
    return BeautifulSoup(page_path.open('rb').read(), 'html.parser').find_all('table')[1]


def get_cached_spain_table():
    page_path: pathlib.Path = pathlib.Path('tests/resources/spain.html')
    return BeautifulSoup(page_path.open('rb').read(), 'html.parser').find_all('table')[2]


def get_cached_sweden_table():
    page_path: pathlib.Path = pathlib.Path('tests/resources/sweden.html')
    return BeautifulSoup(page_path.open('rb').read(), 'html.parser').find_all('table', {'class': 'wikitable'})[0]
