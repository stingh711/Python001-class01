# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from spiders import utils


class MaoyanPipeline:
    def process_item(self, item, spider):
        # with open("movies.csv", "a+", encoding="utf-8") as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow([item["name"], item["time"], item["category"]])
        utils.insert_movie(item["name"], item["time"], item["category"])
        return item
