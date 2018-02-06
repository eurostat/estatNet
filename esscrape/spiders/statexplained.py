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
from scrapy.loader.processors import TakeFirst

from .. import essError, essWarning#analysis:ignore 
from .. import settings
from .. import items

#==============================================================================
# GLOBAL VARIABLES
#==============================================================================

try:
    assert PAGE_CHECK
    assert not (PAGE_CHECK in (None,{}) or all([v in ([],'',None) for v in PAGE_CHECK.values()]))
except (NameError,AssertionError):
    PAGE_CHECK = {}
    PAGE_CHECK['article']   = '//h2[span[contains(text()[normalize-space(.)], "Further Eurostat information")]] \
                                      | //h2[span[contains(text()[normalize-space(.)], "See also")]] \
                                      | //h3[span[contains(text()[normalize-space(.)], "Dedicated section")]]'
    PAGE_CHECK['glossary']  = '//h2[span[contains(text()[normalize-space(.)], "Related concepts")]] \
                                      | //h2[span[contains(text()[normalize-space(.)], "Statistical data")]]'
    PAGE_CHECK['category']  = '//h2[starts-with(text()[normalize-space(.)], "Pages in category")]'
    PAGE_CHECK['theme']     = '//h2[span[@id="Statistical_articles"]]//text()'
              

#==============================================================================
# COMMON METHODS
#==============================================================================

def __check_page(self, response, page):
    if not page in settings.SE_KEYDOMAINS:
        raise essError("Page type %s not recognised as any from Eurostat website" % page)
    else:
        domain = settings.SE_KEYDOMAINS[page]
    if domain not in (None,'',[]):
        return response.url.startswith(domain)
    else:
        return TakeFirst()(response.xpath(PAGE_CHECK[page])) is not None
        
        
def __identify_page(self, response, page):        
    res = False
    for (page,domain) in settings.SE_KEYDOMAINS.items():
        if domain not in (None,'',[]):
            res = response.url.startswith(domain)
        else:
            res = TakeFirst()(response.xpath(PAGE_CHECK[page]))
        if res is True:
            return page
    if res is False: # actually if we are still here...
        #warn(essWarning("Page %s not recognised as a standard type" % response.url))
        return None
        
#==============================================================================
# GLOBAL CLASSES/METHODS/
#==============================================================================
    
class SEWhatLinksHere(scrapy.Spider):
    name = "WhatLinksHere"
    allowed_domains = [settings.SE_MAINURL] 
    
    def __init__(self, page, *args, **kwargs):
        super(SEWhatLinksHere, self).__init__(*args, **kwargs)
        if page is None:
           raise essError("Name of destination page is missing")
        self.start_urls = ['%s/%s&limit=%s' % (settings.WHATLINKSHERE_URL, page, settings.WHATLINKSHERE_LIMIT)]
    
    #def start_requests(self):
    #    yield scrapy.Request('%s/%s&limit=%s' % (settings.WHATLINKSHERE_URL, self.page, settings.WHATLINKSHERE_LIMIT))    
    
class SESpider(scrapy.Spider):
    name = "StatisticalExplained"
    allowed_domains = [settings.SE_MAINURL] 

    def __init__(self, *args, **kwargs):
        attr = [(k, kwargs.pop(k)) for k in settings.SE_KEYDOMAINS if kwargs.get(k) is not None]
        if len(attr) > 1:
           raise essError("Only one key among %s can be accepted" % settings.SE_KEYDOMAINS)
        elif len(attr) == 1:
            attr = attr[0]
            # # normally, the default super.__init__ method which takes any spider 
            # # arguments and copies them to the spider as attributes, however we
            # # filter the kwargs, so we have to create the attribute manually
            # # setattr(self, attr[0], attr[1])
            self.start_urls = ['%s/%s%s' % (settings.SE_MAINURL, settings.SE_KEYDOMAINS[attr[0]], attr[1])]            
        else:
            self.start_urls = ['%s/%s' % (settings.SE_MAINURL, settings.CATEGORIES_DOMAIN)]
        super(SESpider, self).__init__(*args, **kwargs)
        
    #def start_requests(self):
    #    yield scrapy.Request( )
    
    @staticmethod
    def _parse_loader(cls, response):
        l = cls(response=response)
        [l.add_xpath(key, l.item._paths[key]) for key in l.item._allowed_keys]
        return l.load_item()

    def parse_item(self, response):
        self.logger.info('%s', response.url)
        title = response.url.split('/')[-1]
        if title.startswith(settings.GLOSSARY_SUBDOMAIN):
            yield self._parse_loader(items.GlossaryItemLoader, response)
        elif title.startswith(settings.CATEGORY_SUBDOMAIN):
            yield self._parse_loader(items.CategoryItemLoader, response)
        elif title.startswith(settings.ARTICLE_SUBDOMAIN):
            yield self._parse_loader(items.ArticleItemLoader, response)
        
    def _parse_category(self, response):
        #l = CategoryItemLoader(response=response)
        #[l.add_xpath(key, CATEGORY_PATHS[key]) for key in CATEGORY_PATHS.keys()]
        #yield l.load_item()
        yield self._parse_loader(items.CategoryItemLoader, response)

    def _parse_glossary(self, response):
        #l = GlossaryItemLoader(response=response)
        #[l.add_xpath(key, GLOSSARY_PATHS[key]) for key in GLOSSARY_PATHS.keys()]
        #yield l.load_item()
        yield self._parse_loader(items.GlossaryItemLoader, response)

    def _parse_article(self, response):
        #l = ArticleItemLoader(response=response)
        #[l.add_xpath(key, ARTICLE_PATHS[key]) for key in ARTICLE_PATHS.keys()]
        #yield l.load_item()
        yield self._parse_loader(items.ArticleItemLoader, response)


    #def start_requests(self):
    #    yield scrapy.Request('%s/%s:%s' % (settings.SE_MAINURL, settings.CATEGORY_KEY, category))
        
    #def start_requests(self):
    #    urls = [
    #        '%s/%s' % (settings.SE_MAINURL, settings.CATEGORIES_DOMAIN)
    #    ]
    #    for url in urls:
    #        yield scrapy.Request(url=url, callback=self.parse)
    
              
#class StatExplainedCrawler(scrapy.CrawlSpider):
#    name = "StatExplained"
#    allowed_domains = settings.ESTAT_URL
#    start_urls = settings.SE_MAINURL
#
#
#    rules = (
#        Rule(LinkExtractor(restrict_xpath="//ul[@class='nav nav-list']/li/ul/li/a"), follow=True),
#        Rule(LinkExtractor(restrict_xpath="//article[@class='product_pod']/h3/a"), callback="parse_book")
#    )
#    
#
#    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
#    rules = [
#        Rule(
#            LinkExtractor(
#                canonicalize=True,
#                unique=True
#            ),
#            follow=True,
#            callback="parse_items"
#        )
#    ]
#
#    # Method which starts the requests by visiting all URLs specified in start_urls
#    def start_requests(self):
#        for url in self.start_urls:
#            yield scrapy.Request(url, callback=self.parse, dont_filter=True)
#
#    # Method for parsing items
#    def parse_items(self, response):
#        # The list of items that are found on the particular page
#        items = []
#        # Only extract canonicalized and unique links (with respect to the current page)
#        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
#        # Now go through all the found links
#        for link in links:
#            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
#            is_allowed = False
#            for allowed_domain in self.allowed_domains:
#                if allowed_domain in link.url:
#                    is_allowed = True
#            # If it is allowed, create a new item and add it to the list of found items
#            if is_allowed:
#                item = DatabloggerScraperItem()
#                item['url_from'] = response.url
#                item['url_to'] = link.url
#                items.append(item)
#        # Return all the found items
#        return items