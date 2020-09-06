# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from spiders.items import GoodsItem


class SmzdmSpider(scrapy.Spider):
    name = "smzdm"
    allowed_domains = ["smzdm.com"]
    start_urls = ["https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/"]

    def parse(self, response):
        links = (
            Selector(response=response)
            .xpath("//h5[contains(@class, 'feed-block-title')]/a/@href")
            .getall()[:10]
        )
        for link in links:
            item = GoodsItem()
            item["link"] = link
            yield scrapy.Request(
                url=link, meta={"item": item}, callback=self.parse_comments_links
            )

    def parse_comments_links(self, response):
        item = response.meta["item"]
        selector = Selector(response=response)
        name = selector.css("h1.title::text").get().strip()
        item["name"] = name
        links = selector.css(
            "#commentTabBlockNew>ul.pagination>li>a::attr(href)"
        ).getall()
        if links:
            for link in links[:-2]:
                yield scrapy.Request(
                    url=link, meta={"item": item}, callback=self.parse_comments
                )

        yield scrapy.Request(
            url=item["link"], meta={"item": item}, callback=self.parse_comments
        )

    def parse_comments(self, response):
        comment_boxes = Selector(response=response).xpath(
            '//div[@id="commentTabBlockNew"]//div[@class="comment_conBox"]'
        )
        comments = []
        for comment_box in comment_boxes:
            time = comment_box.css("div.time>meta::attr(content)").get()
            comment = (
                comment_box.css(
                    "div.comment_conBox>div.comment_conWrap>div.comment_con>p>span::text"
                )
                .get()
                .strip()
            )
            if comment:
                comments.append({"time": time, "comment": comment})
        item = response.meta["item"]
        item["comments"] = comments
        yield item
