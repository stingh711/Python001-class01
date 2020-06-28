# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from spiders.items import MovieItem


class MaoyanSpider(scrapy.Spider):
    name = "maoyan"
    allowed_domains = ["maoyan.com"]
    start_urls = ["https://maoyan.com/films?showType=3"]

    def parse(self, response):
        print(response.text)
        paths = (
            Selector(response=response)
            .xpath("//div[contains(@class, 'movie-item film-channel')]/a/@href")
            .getall()
        )
        links = [f"https://maoyan.com{path}" for path in paths]
        for link in links:
            item = MovieItem()
            item["link"] = link
            yield scrapy.Request(
                url=link, meta={"item": item}, callback=self.parse_detail
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        selector = Selector(response=response)
        name = (
            selector.xpath("/html/body/div[3]/div/div[2]/div[1]/h1/text()")
            .get()
            .strip()
        )
        time = (
            selector.xpath("/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()")
            .get()
            .strip()
        )
        categories = selector.xpath(
            '//div[contains(@class, "movie-brief-container")]/ul/li[1]/a/text()'
        ).getall()
        category = " ".join([c.strip() for c in categories])
        item["category"] = category
        item["name"] = name
        item["time"] = time
        yield item

