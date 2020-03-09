# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

try:
    import
except:
    import networkx as nx

class Pipeline(object):
    def process_item(self, item, spider):
        return item
