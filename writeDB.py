import requests
from bs4 import BeautifulSoup
from model import Country
from database import SessionLocal
import logging

URL = "https://www.worldometers.info/coronavirus/"

db = SessionLocal()


def fetch_data(url) -> list:
    """
    Gets the data from Worldometers and returns a list with information for
    all existing countries
    """
    site_content = requests.get(url).text
    soup = BeautifulSoup(site_content, 'html.parser')
    table = soup.tbody
    all_links = table.find_all('a')

    countries = [item.text for item in all_links if 'country/' in str(item)]

    tds = [tr for tr in table]

    # Rows before index 17 are empty and only even rows contain data.
    start = tds[17:]
    countries = [y for x, y in enumerate(start) if x % 2 == 0]

    country_data = []

    for country in countries:
        c = []
        for y, x in enumerate(country.find_all('td')):
            c.append(x.text)
        country_data.append(c)

    return country_data


def write_to_db():
    """
    Writes the results from the fetch_data function to the Sqlite Database.
    If the database if already populated it updates the values for each country.
    """
    collect_entries = []
    for idx, c in enumerate(fetch_data(URL)):
        numbers = 0
        if len(c[4]) > 5:
            logging.info(f'len(c[4]) < 6: {numbers}')
            numbers = int(c[4].replace(',', ''))
        if len(c[4]) < 5 and len(c[4]) > 1:
            logging.info(f'{c[4]} between 1 and 1000')
            numbers = c[4]
        if len(c[4]) == 1:
            logging.warning(f'{c[4]} Does not exist')
            numbers = 0

        # Exists or not
        value = db.query(Country).filter(Country.country == c[1]).first()
        if value:
            value.total_cases = int(c[2].replace(',', '')) or 0
            value.new_cases = int(c[3][1:].replace(',', '')) if c[3] else 0
            value.total_deaths = numbers
            value.new_deaths = int(c[5][1:].replace(',', '')) if c[5] else 0
        else:
            collect_entries.append(
                Country(
                    country=c[1],
                    total_cases=int(c[2].replace(',', '')) or 0,
                    new_cases=int(c[3][1:].replace(',', '')) if c[3] else 0,
                    total_deaths=numbers,
                    new_deaths=int(c[5][1:].replace(',', '')) if c[5] else 0,
                    population=int(c[13].replace(',', ''))
                    if ',' in c[13] else 0
                )
            )

    db.add_all(collect_entries)
    db.commit()
    db.close()


if __name__ == '__main__':
    write_to_db()