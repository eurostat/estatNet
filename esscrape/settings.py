#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. _esscrape_settings.py

Common settings and basic definitions for Eurobase scraping/indexing spider defined
in `mod::esscrape` module.  

**About**

For simplicity, this file contains only settings considered important or
commonly used. 

*credits*:      `gjacopo <jacopo.grazzini@ec.europa.eu>`_ 

*version*:      0.1
--
*since*:        Mon Dec 18 17:28:29 2017

**Usage**

    >>> from scrapyroWarning import settings

"""

#%%
#==============================================================================
# GLOBAL VARIABLES USED FOR SETTING THE CONNECTION TO EUROSTAT WEBSITE
#============================================================================== 

PROTOCOL            = 'http'
"""
Webpage protocol.
"""

EC_URL              = 'ec.europa.eu'
"""
European Commission URL.
"""
ESTAT_DOMAIN        = 'eurostat' 
"""
Eurostat domain under European Commission URL.
"""
ESTAT_URL           = '%s://%s/%s' % (PROTOCOL, EC_URL, ESTAT_DOMAIN)
"""
Eurostat complete URL.
"""

def __build_estat_url(domain):
    # return '%s/%s' % (ESTAT_URL, domain)
    return '%s://%s/%s/%s' % (PROTOCOL, EC_URL, ESTAT_DOMAIN, domain)

SE_DOMAINURL        = 'statistics-explained/index.php'
"""
Statistical Explained domain under Eurostat URL.
"""
SE_RELURL           = '%s/%s' % (ESTAT_DOMAIN, SE_DOMAINURL)
"""
Statistical Explained domain under European Commission URL.
"""
SE_MAINURL          = '%s://%s/%s/%s' % (PROTOCOL, EC_URL, ESTAT_DOMAIN, SE_DOMAINURL)
"""
Statistical Explained complete URL.
"""

def __build_se_url(page):
    if page in (None,''):
        return '%s://%s/%s/%s' % (PROTOCOL, EC_URL, ESTAT_DOMAIN, SE_DOMAINURL)
    else:
        # return '%s/%s?%s' % (ESTAT_URL, SE_DOMAINURL, subdomain)
        return '%s://%s/%s/%s?%s' % (PROTOCOL, EC_URL, ESTAT_DOMAIN, SE_DOMAINURL, page)

GLOSSARY_KEY        = 'glossary'
CATEGORY_KEY        = 'category'
ARTICLE_KEY         = 'article'
THEME_KEY           = 'theme'
CONCEPT_KEY         = 'concept'
WHATLINKS_KEY       = 'whatlinks'

SE_KEYS             = [GLOSSARY_KEY, CATEGORY_KEY, ARTICLE_KEY, THEME_KEY, CONCEPT_KEY]

MAIN_PAGE           = 'Main_Page'
"""
Domain of the "Statistics Explained" main page.
"""
#MAIN_PAGE_URL       = __build_se_url(MAIN_PAGE)
#"""
#Full URL of the "Statistics Explained" main page.
#"""

ARTICLES_PAGE       = 'All_articles'
"""
Domain where "All articles" are referred.
"""
#ARTICLES_URL        = __build_se_url(ARTICLES_PAGE)
#"""
#Full URL of the "All articles" page, _e.g._ it is something like this page:
#`<http://ec.europa.eu/eurostat/statistics-explained/index.php/All_articles>`_.
#"""

GLOSSARIES_PAGE     = 'Thematic_glossaries'
"""
Domain of the "Thematic glossaries" page.
"""
#GLOSSARIES_URL      = __build_se_url(GLOSSARIES_PAGE)
#"""
#Full URL of the "Thematic glossaries" page, _e.g._ it is something like this page:
#`<http://ec.europa.eu/eurostat/statistics-explained/index.php/Thematic_glossaries>`_.
#"""

CATEGORIES_PAGE     = 'Special:Categories'
"""
Domain of the "Categories" page.
"""
#CATEGORIES_URL      = __build_se_url(CATEGORIES_PAGE)
#"""
#Full URL of the "Categories" page, _e.g._ it is something like this page:
#`<http://ec.europa.eu/eurostat/statistics-explained/index.php/Special:Categories>`_.
#"""

CONCEPTS_PAGE       = 'Category:Statistical_concept'
"""
Domain of the "Statistical concepts" page.
"""
#CONCEPTS_URL        = __build_se_url(CONCEPTS_PAGE)
#"""
#Full URL of the "Statistical concepts" page, _e.g._ it is something like this page:
#`<http://ec.europa.eu/eurostat/statistics-explained/index.php/Category:Statistical_concept>`_.
#"""

THEMES_PAGE         = 'Statistical_themes'
"""
Domain of the "Statistical themes" page.
"""
#THEMES_URL          = __build_se_url(THEMES_PAGE)
#"""
#Full URL of the "Statistical themes" page, _e.g._ it is something like this page:
#`<http://ec.europa.eu/eurostat/statistics-explained/index.php/Statistical_themes>`_.
#"""

SE_START_PAGES      = {'main':          MAIN_PAGE,
                       GLOSSARY_KEY:    GLOSSARIES_PAGE, 
                       CATEGORY_KEY:    CATEGORIES_PAGE, 
                       ARTICLE_KEY:     ARTICLES_PAGE, 
                       THEME_KEY:       THEMES_PAGE,
                       CONCEPT_KEY:     CONCEPTS_PAGE
                       }
"""Dictionary of Statistics Explained main pages.
"""

SE_START_URLS       =  {k: __build_se_url(v) for k, v in SE_START_PAGES.items()}
"""Dictionary of Statistics Explained main URLs built upon the main pages defined
in :var:`SE_START_PAGES`.
"""

WHATLINKSHERE_PAGE  = 'title=Special:WhatLinksHere'
"""
Domain of the "What link's here" pages.
"""
WHATLINKSHERE_URL   = __build_se_url(WHATLINKSHERE_PAGE)
"""
Full URL of the "What link's here" pages.
"""
WHATLINKSHERE_LIMIT = 500
"""
Upper limit of what can be displayed on a single "What link's here" page.
"""

GLOSSARY_DOMAIN     = 'Glossary:'
"""
String used for naming the URL subdomains of glossary pages, _i.e._ those pages 
that are referenced into the "Glossary" page.
"""
CATEGORY_DOMAIN     = 'Category:'
"""
String used for naming the URL subdomains of category pages, _i.e._ those pages 
that are referenced into the "Category" page.
"""
ARTICLE_DOMAIN      = ''
"""
String used for naming the URL subdomains of article pages, _i.e._ those pages 
that are referenced into the "All articles" page.
"""
THEME_DOMAIN        = ''
"""
String used for naming the URL subdomains of theme pages, _i.e._ those pages 
that are referenced into the "Statistical themes" page.
"""
CONCEPT_DOMAIN      = GLOSSARY_DOMAIN
"""
String used for naming the URL subdomains of concept pages, _i.e._ those pages 
that are referenced into the "Statistical concepts" page.
"""

SE_KEYDOMAINS       = {GLOSSARY_KEY:    GLOSSARY_DOMAIN, 
                       CATEGORY_KEY:    CATEGORY_DOMAIN, 
                       ARTICLE_KEY:     ARTICLE_DOMAIN, 
                       THEME_KEY:       THEME_DOMAIN,
                       CONCEPT_KEY:     CONCEPT_DOMAIN
                       }
"""
"""

API_DOMAIN          = 'ec.europa.eu/eurostat/wdds/rest/data'
"""
Domain of Eurostat API (not used here).
"""

LANGS               = ('en','de','fr')
"""
Languages supported by this package.
"""
DEF_LANG            = 'en'
"""
Default language used when launching Eurostat API.
"""

#==============================================================================
# GLOBAL VARIABLES USED FOR SETTING THE SPIDER/CRAWLER
#==============================================================================

# More Scrapy settings in this documentation:
#   http://doc.scrapy.org/en/latest/topics/settings.html
#   http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#   http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME            = 'scrapyrostat'

SPIDER_MODULES      = ['scrapyrostat.spiders']
NEWSPIDER_MODULE    = 'scrapyrostat.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT          = 'scrapyrostat (+https://github.com/gjacopo/scrapyrostat)'

# Obey robots.txt rules
ROBOTSTXT_OBEY      = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY      = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED    = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'esscrape.middlewares.EsscrapeSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'esscrape.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'esscrape.pipelines.EsscrapePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
