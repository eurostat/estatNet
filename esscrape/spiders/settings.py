#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. settings.py

Basic definitions for Eurobase scraping/indexing spider.

**About**

*credits*:      `gjacopo <jacopo.grazzini@ec.europa.eu>`_ 

*version*:      0.1
--
*since*:        Mon Dec 18 17:28:29 2017

**Contents**
"""


#==============================================================================
# GLOBAL CLASSES/METHODS/VARIABLES
#==============================================================================

PACKAGE         = "esscrape"

ESTAT_URL       = 'ec.europa.eu/eurostat/'
"""
Eurostat URL.
"""

SE_MAINURL      = 'http://ec.europa.eu/eurostat/statistics-explained/index.php'
"""
Statistical Explained main URL.
"""
MAIN_DOMAIN     = 'Main_Page'
"""
Domain of the main page.
"""
ALL_DOMAIN = 'All_articles'
"""
Domain where all articles are referred.
"""
GLOSSARIES_DOMAIN = 'Thematic_glossaries'
"""
Domain of the thematic glossaries.
"""
THEMES_DOMAIN   = 'Statistical_themes'
"""
Domain of the statistical themes.
"""
CATEGORIES_DOMAIN = 'Special:Categories'
"""
Domain of the categories.
"""

GLOSSARY_KEY    = 'Glossary'
CATEGORY_KEY    = 'Category'
THEME_KEY       = ''


API_DOMAIN      = 'ec.europa.eu/eurostat/wdds/rest/data'
"""
Domain of Eurostat API (not used here).
"""

PROTOCOL        = 'http'
"""
Webpage protocol.
"""
LANGS           = ('en','de','fr')
"""
Languages supported by this package.
"""
DEF_LANG        = 'en'
"""
Default language used when launching Eurostat API.
"""
