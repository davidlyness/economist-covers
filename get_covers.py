# coding=utf-8
"""get_covers"""

import bs4
import dateutil.parser
import requests
import sqlite3

import database


def get_covers():
    """
    Get new covers from the Economist website and add them to the database.
    """
    db = database.Database("db.sqlite3")
    base_url = "http://www.economist.com/printedition/covers?print_region=76976"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    soup = bs4.BeautifulSoup(requests.get(base_url, headers=headers).text, "html.parser")
    years = [opt.contents[0] for opt in soup.find("select", {"id": "edit-date-filter-value-year"}).findAll("option")]
    new_covers = True

    for year in years:
        if new_covers:
            year_url = "{}&date_filter%5Bvalue%5D%5Byear%5D={}".format(base_url, year)
            soup = bs4.BeautifulSoup(requests.get(year_url, headers=headers).text, "html.parser")
            for thumbnail_section in soup.findAll("div", {"class": "views-print-cover"}):
                cover_page_path = thumbnail_section.find("div", {"class": "print-cover-links"}).findAll("a")[0]['href']
                cover_page_url = "http://www.economist.com{}".format(cover_page_path)
                cover_date_string = thumbnail_section.find("span", {"class": "date-display-single"}).text
                cover_date = dateutil.parser.parse(cover_date_string)
                cover_soup = bs4.BeautifulSoup(requests.get(cover_page_url, headers=headers).text, "html.parser")
                cover_link = cover_soup.find("div", {"class": "cover-content"}).find("img")['src']
                cover_image = requests.get(cover_link, headers=headers).content
                try:
                    db.add_cover(cover_link, cover_image, cover_date)
                except sqlite3.IntegrityError:
                    new_covers = False
                    break


if __name__ == "__main__":
    get_covers()
