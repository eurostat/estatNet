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

from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst

from collections import Mapping

from .. import scrapError, scrapWarning#analysis:ignore 
from ..settings import DEF_LANG, SE_MAINURL, SE_KEYS, SE_KEYDOMAINS, \
    ARTICLE_KEY, GLOSSARY_KEY, CATEGORY_KEY, THEME_KEY, CONCEPT_KEY,                \
    ARTICLE_DOMAIN, GLOSSARY_DOMAIN, CATEGORY_DOMAIN, THEME_DOMAIN, CONCEPT_DOMAIN, \
    SE_START_PAGES,                                                                 \
    WHATLINKSHERE_URL, WHATLINKSHERE_LIMIT                                          \
    
import items
from ..items import GLOSSARY_PATHS, SE_PAGES_PATHS, SE_START_PAGES_PATHS, WHATLINKS

#%%
#==============================================================================
# GLOBAL VARIABLES
#==============================================================================

try:
    assert PAGE_CHECK
    assert not (PAGE_CHECK in (None,{}) or all([v in ([],'',None) for v in PAGE_CHECK.values()]))
except (NameError,AssertionError):
    PAGE_CHECK = {}
    PAGE_CHECK[ARTICLE_KEY] =                                   \
        '//h2[span[contains(normalize-space(text()), "Further Eurostat information")]] \
            | //h2[span[contains(normalize-space(text()), "See also")]] \
            | //h3[span[contains(normalize-space(text()), "Dedicated section")]]'
    PAGE_CHECK[GLOSSARY_KEY] =                                  \
        '//h1[@id="firstHeading"][starts-with(normalize-space(text()), "Glossary")]   \
            | //h2[span[contains(normalize-space(text()), "Related concepts")]] \
            | //h2[span[contains(normalize-space(text()), "Statistical data")]]'
    PAGE_CHECK[CATEGORY_KEY] =                                  \
        '//h1[@id="firstHeading"][starts-with(normalize-space(text()), "Category")]   \
            | //h2[starts-with(normalize-space(text()), "Pages in category")]'
    PAGE_CHECK[THEME_KEY] =                                     \
        '//h2[span[@id="Statistical_articles"]]//text()'
    PAGE_CHECK[CONCEPT_KEY] =                                   \
        PAGE_CHECK[GLOSSARY_KEY]

#%%
#==============================================================================
# COMMON METHODS
#==============================================================================

def __check_page(response, page):
    if not page in SE_KEYDOMAINS:
        raise scrapError("Page type %s not recognised as any from Eurostat website" % page)
    else:
        domain = SE_KEYDOMAINS[page]
    if domain not in (None,'',[]):
        return response.url.startswith(domain)
    else:
        return TakeFirst()(response.xpath(PAGE_CHECK[page])) is not None
        
        
def __identify_page(response):        
    res = False
    for (page,domain) in SE_KEYDOMAINS.items():
        if domain not in (None,'',[]):
            res = response.url.startswith(domain)
        else:
            res = TakeFirst()(response.xpath(PAGE_CHECK[page]))
        if res is True:
            return page
    if res is False: # actually if we are still here...
        #warn(essWarning("Page %s not recognised as a standard type" % response.url))
        return None
        
def __remove_link(path):
    return path.replace('/a/@href','') # we should use a regex here...    
    
#%%
#==============================================================================
# GLOBAL CLASSES/METHODS/
#==============================================================================
    
class WhatLinksSpider(Spider):
    name = "WhatLinksHere"
    allowed_domains = [SE_MAINURL] 
    
    @staticmethod
    def url_whatlinkshere(page):
        return '%s/%s&limit=%s' % (WHATLINKSHERE_URL, page, WHATLINKSHERE_LIMIT)
    
    def __init__(self, page, *args, **kwargs):
        self.npages, self.nlinks = kwargs.pop('npages', -1), kwargs.pop('nlinks', -1)
        if page is None:
           raise scrapError("Name of destination page is missing")
        elif not isinstance(page, (list, tuple)):
            page = page[0]
        if self.start_urls is None:
            self.start_urls = []
        [self.start_urls.append(self.url_whatlinkshere(p)) for p in page]
        super(WhatLinksSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        #for page in self.page:
        #    yield scrapy.Request(url=self.url_whatlinkshere(self.page), callback=self.parse)  
        for url in getattr(self, 'start_urls', []):
            yield scrapy.Request(url=url, callback=self.parse_whatlinkshere)
            
    def parse_whatlinkshere(self, response):
        self.logger.info('Exploring what links to %s...', response.url)
        # if response.status :
        next_pages = response.xpath(WHATLINKS['Links']).extract()
        whatlink = items.WhatLinksItem(response=response)
        [whatlink.add_xpath(key, whatlink.paths[key]) for key in whatlink.fields]
        yield whatlink
        for next_page in next_pages:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(self.url_whatlinkshere(next_page), callback=self.parse_whatlinkshere)
            
            
class PageCrawler(CrawlSpider):
    name = "PageExplained"
    allowed_domains = [SE_MAINURL]  # [settings.ESTAT_URL]
    allowed_arguments = [key for key in SE_KEYS if key!=ARTICLE_KEY]

    # this spider has one rule per type of page scraped: extract all (unique and 
    # canonicalized) links, follow them and parse them using the dedicated parse
    # method
    rules = (
        Rule(LinkExtractor(restrict_xpath=__remove_link(SE_PAGES_PATHS[key]['Links']), 
                           allow=r"^" + SE_MAINURL + SE_KEYDOMAINS[key],
                           deny=[r"^" + SE_MAINURL + SE_KEYDOMAINS[_]   \
                                 for _ in SE_KEYDOMAINS.keys()          \
                                 if _!=key and SE_KEYDOMAINS[_]!='']), 
             callback="_parse_%s" % key )
        for key in allowed_arguments
        )

    def __init__(self, pages=None, *args, **kwargs):
        self.lang, self.maxdepth = kwargs.pop('lang', DEF_LANG), kwargs.pop('depth',0)
        if pages in (None,{},[]):
            pages = self.allowed_argments # 'main' instesad ? 
        if isinstance(pages,str) and pages in self.allowed_arguments:
            pages = {pages: True}
        elif isinstance(pages,(list,tuple))     \
                and set(pages).difference(set(self.allowed_arguments)) == set({}):
            pages = {(key,True) for key in self.allowed_arguments} # {'main': True} ? 
        elif not isinstance(pages,Mapping)      \
                or set(pages.keys()).difference(set(self.allowed_arguments)) != set({}):
            raise scrapError('wrong settings for PAGES parameter')
        #if set(self.allowed_argments).intersection(set(pages.keys())) == set({}):
        #    warning.warn(scrapWarning('nothing to scrape!'))
        #    return
        self.start_urls = []
        [self.start_urls.append(SE_START_PAGES[key] if val is True  
                                else '%s/%s%S' % (SE_MAINURL, SE_KEYDOMAINS[key], val))
            for (key,val) in pages.items() ] 
        super(PageCrawler, self).__init__(*args, **kwargs)

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_start_url(self, response):
        key = __identify_page(response) 
        if response.url == SE_START_PAGES[key]:
            links = response.xpath(SE_START_PAGES_PATHS[key]['Links'])
        else:
            links = response.xpath(SE_PAGES_PATHS[key]['Links'])
        for link in links:
            yield scrapy.Request(link, callback=self.parse) # ???? 
    
        
    @staticmethod
    def _parse_loader(cls, response):
        l = cls(response=response)
        [l.add_xpath(key, l.item._paths[key]) for key in l.item._allowed_keys]
        return l.load_item()

    def parse_item(self, response):
        self.logger.info('%s', response.url)
        title = response.url.split('/')[-1]
        if title.startswith(GLOSSARY_DOMAIN):
            yield self._parse_loader(items.GlossaryItemLoader, response)
        elif title.startswith(CATEGORY_DOMAIN):
            yield self._parse_loader(items.CategoryItemLoader, response)
        elif title.startswith(ARTICLE_DOMAIN):
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
    