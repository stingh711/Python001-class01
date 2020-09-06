# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
from snownlp import SnowNLP
from datetime import datetime


class SmzdmPipeline:
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host="127.0.0.1", user="postgres", password="111111", dbname="smzdm"
        )
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def _find_product(self, name):
        self.cur.execute("select id from comments_product where name = %s", (name,))
        result = self.cur.fetchone()
        if result:
            return result[0]
        return None

    def _insert_product(self, name):
        self.cur.execute(
            "insert into comments_product (name) values (%s) returning id", (name,),
        )
        self.connection.commit()
        return self.cur.fetchone()[0]

    def process_item(self, item, spider):
        name = item["name"]
        product_id = self._find_product(name)
        if not product_id:
            product_id = self._insert_product(name)
        for comment in item["comments"]:
            s = SnowNLP(comment["comment"])
            time_string = comment["time"]
            date = datetime.strptime(time_string, "%Y-%m-%d").date()

            self.cur.execute(
                "insert into comments_comment (content, product_id, sentiments, timestamp) values (%s, %s, %s, %s)",
                (comment["comment"], product_id, s.sentiments, date),
            )
        self.connection.commit()
        return item
