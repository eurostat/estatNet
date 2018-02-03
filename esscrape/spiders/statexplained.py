#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. settings.py

Basic definitions for Eurobase scraping/indexing spider.

**About**

*credits*:      `gjacopo <jacopo.grazzini@ec.europa.eu>`_ 

*version*:      0.1
--
*since*:        Sun Jan 14 17:31:51 2018

**Contents**
"""

import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .. import settings
from .. import items

#==============================================================================
# GLOBAL VARIABLES
#==============================================================================

#==============================================================================
# GLOBAL CLASSES/METHODS/
#==============================================================================

def _parse_loader(cls, response):
    l = cls(response=response)
    [l.add_xpath(key, l.item._paths[key]) for key in l.item._allowed_keys]
    return l.load_item()
    

class SECategorySpider(scrapy.Spider):
    name = "SECategory"
    allowed_domains = [settings.SE_RELURL] # [SE_MAINURL]

    def __init__(self, category=None, *args, **kwargs):
        super(SECategorySpider, self).__init__(*args, **kwargs)
        if category is None:
            self.start_urls = '%s/%s' % (settings.SE_MAINURL, settings.CATEGORIES_DOMAIN)
        else:
            self.start_urls = '%s/%s:%s' % (settings.SE_MAINURL, settings.CATEGORY_KEY, category)

    def parse_glossary(self, response):
        #l = GlossaryItemLoader(response=response)
        #[l.add_xpath(key, GLOSSARY_PATHS[key]) for key in GLOSSARY_PATHS.keys()]
        #yield l.load_item()
        yield _parse_loader(items.GlossaryItemLoader, response)

    def parse_article(self, response):
        #l = ArticleItemLoader(response=response)
        #[l.add_xpath(key, ARTICLE_PATHS[key]) for key in ARTICLE_PATHS.keys()]
        #yield l.load_item()
        yield _parse_loader(items.ArticleItemLoader, response)

    def parse_category(self, response):
        #l = CategoryItemLoader(response=response)
        #[l.add_xpath(key, CATEGORY_PATHS[key]) for key in CATEGORY_PATHS.keys()]
        #yield l.load_item()
        yield _parse_loader(items.CategoryItemLoader, response)


    #def start_requests(self):
    #    yield scrapy.Request('%s/%s:%s' % (settings.SE_MAINURL, settings.CATEGORY_KEY, category))
        
    #def start_requests(self):
    #    urls = [
    #        '%s/%s' % (settings.SE_MAINURL, settings.CATEGORIES_DOMAIN)
    #    ]
    #    for url in urls:
    #        yield scrapy.Request(url=url, callback=self.parse)
    
              
class StatExplainedCrawler(scrapy.CrawlSpider):
    name = "StatExplained"
    allowed_domains = settings.ESTAT_URL
    start_urls = settings.SE_MAINURL


    rules = (
        Rule(LinkExtractor(restrict_xpath="//ul[@class='nav nav-list']/li/ul/li/a"), follow=True),
        Rule(LinkExtractor(restrict_xpath="//article[@class='product_pod']/h3/a"), callback="parse_book")
    )
    

    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # Method for parsing items
    def parse_items(self, response):
        # The list of items that are found on the particular page
        items = []
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        # Now go through all the found links
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            # If it is allowed, create a new item and add it to the list of found items
            if is_allowed:
                item = DatabloggerScraperItem()
                item['url_from'] = response.url
                item['url_to'] = link.url
                items.append(item)
        # Return all the found items
        return items