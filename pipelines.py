# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class UnsplashPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.unsplash

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class CustomImagesPipline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image'])

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{item['title']}.jpg"
