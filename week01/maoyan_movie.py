import requests
import lxml
import pandas as pd
from bs4 import BeautifulSoup as bs
import csv

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0"
}


def get_list():
    r = requests.get("https://maoyan.com/films?showType=3", headers=HEADERS)
    print(r.text)
    soup = bs(r.text, "html.parser")
    movies = soup.find_all("div", attrs={"class", "movie-item"})[:10]
    return [f"https://maoyan.com{m.find('a').get('href')}" for m in movies]


def get_detail(url):
    r = requests.get(url, headers=HEADERS)
    print(r.text)
    print(url)
    selector = lxml.etree.HTML(r.text)
    name = selector.xpath("/html/body/div[3]/div/div[2]/div[1]/h1/text()")[0].strip()
    time = selector.xpath("/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()")[
        0
    ].strip()
    categories = selector.xpath(
        '//div[contains(@class, "movie-brief-container")]/ul/li[1]/a/text()'
    )
    category = " ".join([c.strip() for c in categories])
    with open("movies.csv", "a+", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, time, category])


if __name__ == "__main__":
    urls = get_list()
    for url in urls:
        get_detail(url)
