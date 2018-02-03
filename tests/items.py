#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. _base_items.py

*credits*:      `gjacopo <jacopo.grazzini@ec.europa.eu>`_ 

*version*:      0.1
--
*since*:        Sun Jan 21 14:21:34 2018

**Contents**
"""

import scrapy
from scrapy import http
from scrapy.loader.processors import TakeFirst

from esscrape import items

_xp = lambda sel, path: sel.xpath(path).extract()
try:
    from esscrape.items import xpath
except ImportError:
    _xpcreate = lambda **kwargs: None
else:
    _xpcreate = lambda **kwargs: xpath.create(**kwargs)
    
import time
import unittest

#/************************************************************************/
class xpathTestCase(unittest.TestCase):
    """Class providing the various tests used when developping the items.xpath class.
    """
    
    def test00_setup(cls):
        return
    
    def test01(self):
        self.assertEqual(_xpcreate(last='LAST',
                                     preceding=True),
                        '//LAST/preceding::*'
                        )
    def test02(self):
        self.assertEqual(_xpcreate(first='FIRST',
                                     following=True),
                        '//FIRST/following::*'
                        )
    def test03(self):
        self.assertEqual(_xpcreate(node='NODE',
                                     first='FIRST',
                                     tag='TAG',
                                     sep='//'),
                        '//NODE//FIRST//TAG'
                        )
    def test04(self):
        self.assertEqual(_xpcreate(node='NODE',
                                     last='LAST',
                                     child=True,
                                     first='FIRST',
                                     tag='TAG',
                                     sep='//'),
                        '//NODE//LAST//preceding::FIRST//TAG'
                        )
    def test05(self): # this one is dummy because preceding_sibling is passed but not last
        self.assertEqual(_xpcreate(node='NODE',
                                     preceding_sibling=True,
                                     first='FIRST',
                                     tag='TAG',
                                     sep='//'),
                        '//NODE//FIRST//TAG' # that's the "least bad" output we can get
                        )
    def test06(self):
        self.assertEqual(_xpcreate(node='NODE',
                                     preceding_sibling=True,
                                     last='LAST',
                                     tag='//TAG',
                                     sep='//'),
                        '//NODE//LAST//preceding-sibling::*//TAG' 
                        )
    def test07(self):
        self.assertEqual(_xpcreate(node='NODE',
                                     following_sibling=True,
                                     first='FIRST',
                                     tag='//TAG',
                                     sep='//'),
                        '//NODE//FIRST//following-sibling::*//TAG' 
                        )
    def test08(self):
        self.assertEqual(_xpcreate(node='NODE',
                                     preceding_sibling='PRECEDING_SIBLING', 
                                     first='FIRST',
                                     tag='TAG',
                                     sep='//'),
                        '//NODE//FIRST//*[preceding-sibling::PRECEDING_SIBLING]//TAG' 
                        )
    def test09(self):
        self.assertEqual(_xpcreate(node='NODE',                                    
                                     first='FIRST',                                    
                                     tag='TAG',                                
                                     identifier='IDENTIFIER',  
                                     ancestor='ANCESTOR',                           
                                     descendant=True,
                                     ),
                        '//NODE/FIRST[IDENTIFIER]/descendant::*[ancestor::ANCESTOR[IDENTIFIER]]/TAG' 
                        )
    def test10(self):
        self.assertEqual(_xpcreate(node='NODE',                                    
                                     first='FIRST',                                    
                                     tag='TAG',                                
                                     identifier='IDENTIFIER',  
                                     ancestor='ANCESTOR',                           
                                     ),
                        '//NODE/FIRST[IDENTIFIER]/*[ancestor::ANCESTOR[IDENTIFIER]]/TAG' 
                        )
    def test11(self):
        self.assertEqual(_xpcreate(node='NODE',
                                     last='LAST',
                                     child='CHILD',
                                     preceding_sibling='/',
                                     sep='//'),
                        '//NODE//LAST/preceding-sibling::CHILD'
                        )
    def test12(self):
        self.assertEqual(_xpcreate(node='NODE',
                                     last='LAST',
                                     child='//CHILD',
                                     preceding_sibling='/',
                                     sep='//'),
                        '//NODE//LAST/preceding-sibling::*[//CHILD]'
                        )
    def test13(self):
        self.assertEqual(_xpcreate(first='FIRST',
                                     tag='TAG',
                                     identifier='IDENTIFIER',
                                     ancestor='ANCESTOR',                           
                                     following_sibling=True,
                                     sep='//'),
                        '//FIRST[IDENTIFIER]//following-sibling::*[ancestor::ANCESTOR[IDENTIFIER]]//TAG'
                        )
    def test14(self):
        self.assertEqual(_xpcreate(node='NODE',
                                     first='FIRST',
                                     last='LAST',
                                     tag='TAG',
                                     identifier='IDENTIFIER',
                                     following_sibling=True,
                                     sep='//'),
                        '//NODE//LAST[IDENTIFIER]//preceding::FIRST[IDENTIFIER]//following-sibling::TAG'
                        )
    def test15(self):
        self.assertEqual(_xpcreate(tag='TAG',
                                     first='FIRST',
                                     following_sibling=True,
                                     sep='//'),
                        '//FIRST//following-sibling::TAG'
                        )
    def test16(self):
        self.assertEqual(_xpcreate(tag='TAG',
                                     node='NODE',
                                     following_sibling='FOLLOWING_SIBLING',
                                     sep='//'),
                        '//NODE//following-sibling::FOLLOWING_SIBLING//TAG'
                        )
    def test21(self):
        self.assertEqual(_xpcreate(node='div[@id="footer"]',
                                     first='li[@id="lastmod"]',
                                     tag='text()',
                                     sep='//'),
                        '//div[@id="footer"]//li[@id="lastmod"]//text()'
                        )
    def test22(self):
        self.assertEqual(_xpcreate(first='h2',
                                     tag='a/@href',
                                     identifier='span[@id="See_also"]',
                                     preceding_sibling='*[starts-with(name(),"h")][1]',
                                     following_sibling='//'),
                        '//h2[span[@id="See_also"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="See_also"]]]/a/@href'
                        )
    def test23(self):
        self.assertEqual(_xpcreate(first='h2',
                                     tag='a/@href',
                                     identifier='span[@id="See_also"]',
                                     preceding_sibling='*[starts-with(name(),"h")][1]',
                                     descendant='/',
                                     sep='//'),
                        '//h2[span[@id="See_also"]]/descendant::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="See_also"]]]//a/@href'
                        )
    def test24(self):
        self.assertEqual(_xpcreate(first='h2',
                                     tag='a/@href',
                                     identifier='span[@id="See_also"]',
                                     ancestor='*[starts-with(name(),"h")][1]',
                                     descendant='/',
                                     sep='//'),
                        '//h2[span[@id="See_also"]]/descendant::*[ancestor::*[starts-with(name(),"h")][1][span[@id="See_also"]]]//a/@href'
                        )
    def test25(self):
        self.assertEqual(_xpcreate(first='h2',
                                     tag='//a/@href',
                                     identifier='span[@id="See_also"]',
                                     ancestor='*[starts-with(name(),"h")][1]',
                                     descendant=True
                                     ),
                        '//h2[span[@id="See_also"]]/descendant::*[ancestor::*[starts-with(name(),"h")][1][span[@id="See_also"]]]//a/@href'
                        )
    def test26(self):
        self.assertEqual(_xpcreate(first='h2',
                                     tag='a/@href',
                                     identifier='span[@id="See_also"]',
                                     ancestor='*[starts-with(name(),"h")][1]',
                                     descendant=True,
                                     sep='//'),
                        '//h2[span[@id="See_also"]]//descendant::*[ancestor::*[starts-with(name(),"h")][1][span[@id="See_also"]]]//a/@href'
                        )
    def test27(self):
        self.assertEqual(_xpcreate(node='div[@id="bodyContent"]',
                                     last='h2[span[@id="Related_concepts"]]',
                                     child='//div[@id="mw-content-text"]',
                                     preceding_sibling='/',
                                     sep='//'),
                        '//div[@id="bodyContent"]//h2[span[@id="Related_concepts"]]/preceding-sibling::*[//div[@id="mw-content-text"]]'
                        )
    def test28(self):
        self.assertEqual(_xpcreate(first='h1[@id="firstHeading"]', 
                                     tag='text()[normalize-space(.)]'),
                        '//h1[@id="firstHeading"]/text()[normalize-space(.)]'
                        )
    def test29(self):
        self.assertEqual(_xpcreate(first='h1[@id="firstHeading"]', 
                                     tag='text()[normalize-space(.)]'),
                        '//h1[@id="firstHeading"]/text()[normalize-space(.)]'
                        )
    def test30(self):
        self.assertEqual(_xpcreate(first='h1[@id="firstHeading"]', 
                                     tag='text()[normalize-space(.)]',
                                     sep='//'),
                        '//h1[@id="firstHeading"]//text()[normalize-space(.)]'
                        )

    @classmethod
    def runtest(cls, **kwargs):
        print('\n{}: Class test %s for testing callable _xpcreate method of items.py' % cls.__name__)
        time.sleep(0.5) 
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        unittest.TextTestRunner(verbosity=kwargs.pop('verbosity',2)).run(suite)
        return
      
#%%        
# ArticleItemTestCase    
class ArticleItemTestCase(unittest.TestCase):
    # Test using a specific example of SE article: 
    # http://ec.europa.eu/eurostat/statistics-explained/index.php/Income_distribution_statistics
    #
    # launch:
    # scrapy shell 'http://ec.europa.eu/eurostat/statistics-explained/index.php/Income_distribution_statistics'
    response = http.HtmlResponse(url="", encoding='utf-8', body=b"""
            <html>
            <body>
            <h1 id="firstHeading" class="firstHeading">Income distribution statistics</h1>
            <div id="footer" role="contentinfo">
                <ul id="f-list" class="list-inline"> 
                    <li id="lastmod"> This page was last modified on 19 September 2017, at 10:19.</li>
                </ul>
            </div>
            </body>
            </html>
            <div id='catlinks' class='catlinks'>
                <div id="mw-normal-catlinks" class="mw-normal-catlinks">
                <a href="/eurostat/statistics-explained/index.php/Special:Categories" title="Special:Categories">Categories</a>: 
                <ul>
                    <li><a href="/eurostat/statistics-explained/index.php/Category:Household_income,_expenditure_and_debt" title="Category:Household income, expenditure and debt">Household income, expenditure and debt</a></li>
                    <li><a href="/eurostat/statistics-explained/index.php/Category:Living_conditions" title="Category:Living conditions">Living conditions</a>
                    </li><li><a href="/eurostat/statistics-explained/index.php/Category:Statistical_article" title="Category:Statistical article">Statistical article</a></li>
                    <li><a href="/eurostat/statistics-explained/index.php/Category:Yearbook" title="Category:Yearbook">Yearbook</a></li>
                </ul>
            </div>
            <div id="mw-hidden-catlinks" class="mw-hidden-catlinks mw-hidden-cats-hidden">Hidden category: 
                <ul>
                    <li><a href="/eurostat/statistics-explained/index.php/Category:Unit_F4" title="Category:Unit F4">Unit F4</a></li>
                </ul>
            </div>
            """)
    
    def test00_setup(self):
        pass
    
    # def test01_constructor_errors(self):
    #     l = items.ArticleItem()
    #     self.assertRaises(RuntimeError, l.add_xpath, 'url', '//a/@href')

    # Title
    #   <h1 id="firstHeading" class="firstHeading">Income distribution statistics</h1>
    # or
    #   <title>Income distribution statistics - Statistics Explained</title>
    def test01(self):
        sel = scrapy.Selector(text='<h1 id="firstHeading" class="firstHeading">Income distribution statistics</h1>')
        self.assertEqual(TakeFirst()(_xp(sel, items.ARTICLE_PATHS['Title'])),
                         'Income distribution statistics')
    def test01_constructor_with_selector(self):
        sel = scrapy.Selector(text='<html><body><h1 id="firstHeading" class="firstHeading">Income distribution statistics</h1></body></html>')
        l = items.ArticleItemLoader(selector=sel)
        self.assertTrue(l.selector is sel)
        l.add_xpath('Title', items.ARTICLE_PATHS['Title'])
        self.assertEqual(l.get_output_value('Title'), 
                         ['Income distribution statistics'])
    def test01_constructor_with_response(self):
        l = items.ArticleItemLoader(response=self.response)
        self.assertTrue(l.selector)
        l.add_xpath('Title', items.ARTICLE_PATHS['Title'])
        self.assertEqual(l.get_output_value('Title'), 
                         ['Income distribution statistics'])  
    
    # Last_modified
    #   <div id="footer" role="contentinfo">
    #   	<ul id="f-list" class="list-inline">
    #   		<li id="lastmod"> This page was last modified on 19 September 2017, at 10:19.</li>
    #        <!-- ... -->
    #   	</ul>
    #   </div>
    def test02(self):
        sel = scrapy.Selector(text='<div id="footer" role="contentinfo"><ul id="f-list" class="list-inline"> \
                              <li id="lastmod"> This page was last modified on 19 September 2017, at 10:19.</li>\
                              </ul></div>')
        self.assertEqual(TakeFirst()(_xp(sel, items.ARTICLE_PATHS['Last_modified'])),
                         ' This page was last modified on 19 September 2017, at 10:19.'
                        )
    # then one will have to run:
    #       import datefinder 
    #       [d for d in datefinder.find_dates(txt)][0]
    # so as to retrieve the (formatted) date-time (e.g.: datetime.datetime(2017, 9, 19, 10, 19))

    # Categories
    #   <div id='catlinks' class='catlinks'>
    #   <div id="mw-normal-catlinks" class="mw-normal-catlinks">
    #   <a href="/eurostat/statistics-explained/index.php/Special:Categories" title="Special:Categories">Categories</a>: 
    #   <ul>
    #   <li><a href="/eurostat/statistics-explained/index.php/Category:Household_income,_expenditure_and_debt" title="Category:Household income, expenditure and debt">Household income, expenditure and debt</a></li>
    #   <li><a href="/eurostat/statistics-explained/index.php/Category:Living_conditions" title="Category:Living conditions">Living conditions</a>
    #   </li><li><a href="/eurostat/statistics-explained/index.php/Category:Statistical_article" title="Category:Statistical article">Statistical article</a></li>
    #   <li><a href="/eurostat/statistics-explained/index.php/Category:Yearbook" title="Category:Yearbook">Yearbook</a></li>
    #   </ul>
    #   </div>
    #   <div id="mw-hidden-catlinks" class="mw-hidden-catlinks mw-hidden-cats-hidden">Hidden category: 
    #   <ul>
    #   <li><a href="/eurostat/statistics-explained/index.php/Category:Unit_F4" title="Category:Unit F4">Unit F4</a></li>
    #   </ul>
    #   </div>
    # running:
    #       urls=response.xpath(ARTICLE_PATHS['Categories']).extract()
    # will return: 
    
    #   urls = ['/eurostat/statistics-explained/index.php/Category:Household_income,_expenditure_and_debt',
    #           '/eurostat/statistics-explained/index.php/Category:Living_conditions',
    #           '/eurostat/statistics-explained/index.php/Category:Statistical_article',
    #           '/eurostat/statistics-explained/index.php/Category:Yearbook']
    
    ## Hidden_categories
    #   <div id="mw-hidden-catlinks" class="mw-hidden-catlinks mw-hidden-cats-hidden">Hidden category: 
    #   <ul>
    #   <li><a href="/eurostat/statistics-explained/index.php/Category:Unit_F4" title="Category:Unit F4">Unit F4</a></li>
    #   </ul>
    #   </div>
    # running:
    #       urls=response.xpath(ARTICLE_PATHS['Categories']).extract()
    # will return: 
    #   urls = ['/eurostat/statistics-explained/index.php/Category:Unit_F4']
        
    ## Source_datasets:
    #   <i>Source:</i> Eurostat  <a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=ilc_li01&amp;language=en&amp;mode=view">(ilc_li01)</a> and  <a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=ilc_li02&amp;language=en&amp;mode=view">(ilc_li02)</a>
    #   ...
    # then, in the scrapy shell, running:
    #       urls=response.xpath(ARTICLE_PATHS['Source_datasets']).extract()
    # will return:
    #   urls = ['http://ec.europa.eu/eurostat/product?code=ilc_li01&language=en&mode=view',
    #           'http://ec.europa.eu/eurostat/product?code=ilc_li02&language=en&mode=view',
    #           'http://ec.europa.eu/eurostat/product?code=ilc_li04&language=en&mode=view',
    #           'http://ec.europa.eu/eurostat/product?code=ilc_li03&language=en&mode=view',
    #           'http://ec.europa.eu/eurostat/product?code=ilc_li03&language=en&mode=view',
    #           'http://ec.europa.eu/eurostat/product?code=ilc_li02&language=en&mode=view',
    #           'http://ec.europa.eu/eurostat/product?code=ilc_di11&language=en&mode=view',
    #           'http://ec.europa.eu/eurostat/product?code=ilc_pnp2&language=en&mode=view',
    #           'http://ec.europa.eu/eurostat/product?code=ilc_li11&language=en&mode=view']    
    
    ## See_also:
    #   <h2><span class="mw-headline" id="See_also">See also</span></h2>
    #   <ul>
    #   <li><a href="/eurostat/statistics-explained/index.php/Children_at_risk_of_poverty_or_social_exclusion" title="Children at risk of poverty or social exclusion">Children at risk of poverty or social exclusion</a></li>
    #   <li><a href="/eurostat/statistics-explained/index.php/Housing_conditions" title="Housing conditions">Housing conditions</a></li>
    #   <li><a href="/eurostat/statistics-explained/index.php/Housing_statistics" title="Housing statistics">Housing statistics</a></li>
    #   <li><a href="/eurostat/statistics-explained/index.php/People_at_risk_of_poverty_or_social_exclusion" title="People at risk of poverty or social exclusion">People at risk of poverty or social exclusion</a></li>
    #   <li><a href="/eurostat/statistics-explained/index.php/Social_inclusion_statistics" title="Social inclusion statistics">Social inclusion statistics</a></li>
    #   </ul>
    #   <h2><span class="mw-headline" id="Further_Eurostat_information">Further Eurostat information</span></h2>
    # running:
    #       urls=response.xpath(ARTICLE_PATHS['See_also']).extract()
    # will return: 
    #   urls = ['/eurostat/statistics-explained/index.php/Children_at_risk_of_poverty_or_social_exclusion',
    #           '/eurostat/statistics-explained/index.php/Housing_conditions',
    #           '/eurostat/statistics-explained/index.php/Housing_statistics',
    #           '/eurostat/statistics-explained/index.php/People_at_risk_of_poverty_or_social_exclusion',
    #           '/eurostat/statistics-explained/index.php/Social_inclusion_statistics']
    
    ## Publications:
    #   <h3><span class="mw-headline" id="Publications">Publications</span></h3>
    #   <p><b>Statistical books</b>
    #   </p>
    #   <ul>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-DZ-14-001&amp;language=en">Living conditions in Europe — 2014 edition</a></li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-FP-13-001&amp;language=en">European social statistics — 2013 edition</a></li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-31-10-555&amp;language=en">Income and living conditions in Europe — 2010 edition</a></li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-EP-09-001&amp;language=en">Combating poverty and social exclusion. A statistical portrait of the European Union 2010</a></li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-80-07-135&amp;language=en">The life of women and men in Europe — A statistical portrait</a></li>
    #   </ul>
    #   <p><b>News releases</b>
    #   </p>
    #   <ul>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=3-17102016-BP&amp;language=en">The share of persons at risk of poverty or social exclusion in the EU back to its pre-crisis level</a></li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=3-16102015-CP&amp;language=en">The risk of poverty or social exclusion affected 1 in 4 persons in the EU in 2014</a></li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=3-04112014-BP&amp;language=en">More than 120 million persons at risk of poverty or social exclusion in 2013</a></li>
    #   </ul>
    #   <p><b>Statistics in focus</b>
    #   </p>
    #   <ul>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-SF-14-012&amp;language=en">Income inequality: nearly 40 per cent of total income goes to people belonging to highest (fifth) quintile</a> — Statistics in focus 12/2014</li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-SF-13-027&amp;language=en">Is the likelihood of poverty inherited?</a> — Statistics in focus 27/2013</li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-SF-13-008&amp;language=en">Living standards falling in most Member States</a> — Statistics in focus 8/2013</li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-SF-13-004&amp;language=en">Children were the age group at the highest risk of poverty or social exclusion in 2011</a> — Statistics in focus 4/2013</li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-SF-12-014&amp;language=en">In 2009 a 6.5&#160;% rise in per capita social protection expenditure matched a 6.1&#160;% drop in EU-27 GDP</a> — Statistics in focus 14/2012</li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-SF-12-009&amp;language=en">23&#160;% of EU citizens were at risk of poverty or social exclusion in 2010</a> — Statistics in focus 9/2012</li>
    #   </ul>
    #   <h3><span class="mw-headline" id="Main_tables">Main tables</span></h3>
    # running:
    #       urls=response.xpath(ARTICLE_PATHS['Publications']).extract()
    # will return: 
    #   urls = ['http://ec.europa.eu/eurostat/product?code=KS-DZ-14-001&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-FP-13-001&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-31-10-555&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-EP-09-001&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-80-07-135&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=3-17102016-BP&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=3-16102015-CP&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=3-04112014-BP&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-SF-14-012&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-SF-13-027&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-SF-13-008&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-SF-13-004&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-SF-12-014&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-SF-12-009&language=en']
    # that works as well:    
    #   urls=response.xpath('//h3[span[@id="Publications" and normalize-space(.)="Publications"]]//following-sibling::ul//li/a/@href').extract()
       
    ## Main_tables
    #   <h3><span class="mw-headline" id="Main_tables">Main tables</span></h3>
    #   <ul>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/web/income-and-living-conditions/data/main-tables">Income and living conditions (t_ilc)</a></li>
    #   </ul>
    #   <h3><span class="mw-headline" id="Database">Database</span></h3>
    # running:
    #       urls=response.xpath(ARTICLE_PATHS['Main_tables']).extract()
    # will return: 
    #   urls = ['http://ec.europa.eu/eurostat/web/income-and-living-conditions/data/main-tables'
        
    ## Database     
    #   <h3><span class="mw-headline" id="Database">Database</span></h3>
    #   <dl>
    #   <dd><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/web/income-and-living-conditions/data/database">Income and living conditions (ilc)</a>, see:</dd>
    #   <dd>Income distribution and monetary poverty (ilc_ip)
    #      <dl>
    #      <dd>Monetary poverty (ilc_li)</dd>
    #      <dd>Monetary poverty for elderly people (ilc_pn)</dd>
    #      <dd>In-work poverty (ilc_iw)</dd>
    #      <dd>Distribution of income (ilc_di)</dd>
    #      </dl>
    #   </dd>
    #   </dl>
    #   <h3><span class="mw-headline" id="Dedicated_section">Dedicated section</span></h3>
    # running:
    #       urls=response.xpath(ARTICLE_PATHS['Database']).extract()
    # will return: 
    #   urls = ['http://ec.europa.eu/eurostat/web/income-and-living-conditions/data/database']
    
    ## Dedicated_section
    #   <h3><span class="mw-headline" id="Dedicated_section">Dedicated section</span></h3>
    #   <ul>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/web/income-and-living-conditions/overview">Income and living conditions</a></li>
    #   </ul>
    #   <h3><span class="mw-headline" id="Methodology_.2F_Metadata">Methodology / Metadata</span></h3>
    # running:
    #       urls=response.xpath(ARTICLE_PATHS['Dedicated_section']).extract()
    # will return: 
    #   urls = ['http://ec.europa.eu/eurostat/web/income-and-living-conditions/overview']
    
    ## Metadata
    #   <h3><span class="mw-headline" id="Methodology_.2F_Metadata">Methodology / Metadata</span></h3>
    #   <ul>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/cache/metadata/en/ilc_esms.htm">Income and living conditions</a> (ESMS metadata file — ilc_esms)</li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-RA-07-007&amp;language=en">Comparative EU Statistics on Income and Living Conditions: Issues and Challenges</a> (Proceedings of the International Conference on EU Comparative Statistics on Income and Living Conditions, Helsinki, 6–8 November 2006)</li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-RA-13-014&amp;language=en">Individual employment, household employment and risk of poverty in the EU — A decomposition analysis</a> — 2013 edition</li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-RA-13-007&amp;language=en">Statistical matching of EU-SILC and the Household Budget Survey to compare poverty estimates using income, expenditures and material deprivation</a> — 2013 edition</li>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-RA-13-010&amp;language=en">Using EUROMOD to nowcast poverty risk in the European Union</a> — 2013 edition</li>
    #   </ul>
    #   <h3><span class="mw-headline" id="Source_data_for_tables_and_figures_.28MS_Excel.29">Source data for tables and figures (MS Excel)</span></h3>
    # running:
    #       urls=response.xpath(ARTICLE_PATHS['Metadata']).extract()
    # will return: 
    #   urls = ['http://ec.europa.eu/eurostat/cache/metadata/en/ilc_esms.htm',
    #           'http://ec.europa.eu/eurostat/product?code=KS-RA-07-007&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-RA-13-014&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-RA-13-007&language=en',
    #           'http://ec.europa.eu/eurostat/product?code=KS-RA-13-010&language=en']
    
    ## External_links: 
    #   <h2><span class="mw-headline" id="External_links">External links</span></h2>
    #   <ul>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/social/main.jsp?langId=en&amp;catId=113#ESDE">Employment and social analysis</a>, see:
    #       <ul>
    #       <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/social/main.jsp?catId=738&amp;langId=en&amp;pubId=7952&amp;type=2&amp;furtherPubs=yes">European Commission — Directorate-General for Employment, Social Affairs &amp; Inclusion — Employment and Social Development in Europe (2016)</a></li>
    #       <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/social/main.jsp?catId=737&amp;langId=en&amp;pubId=7979&amp;furtherPubs=yes">European Commission — Directorate-General for Employment, Social Affairs &amp; Inclusion — Employment and Social Development in Europe — Quarterly Review — Winter 2016</a></li>
    #       </ul>
    #       </li>
    #       <li><a rel="nofollow" class="external text" href="http://www.oecd.org/statistics/better-life-initiative.htm">OECD — Better Life Initiative: Measuring Well-being and Progress</a>
    #   </li>
    #   </ul>
    # running:
    #       urls=response.xpath(ARTICLE_PATHS['External_links']).extract()
    # will return: 
    #   urls = ['http://ec.europa.eu/social/main.jsp?langId=en&catId=113#ESDE',
    #           'http://ec.europa.eu/social/main.jsp?catId=738&langId=en&pubId=7952&type=2&furtherPubs=yes',
    #           'http://ec.europa.eu/social/main.jsp?catId=737&langId=en&pubId=7979&furtherPubs=yes',
    #           'http://www.oecd.org/statistics/better-life-initiative.htm']    
    # that works as well:    
    #   urls=response.xpath('//h2[span[@id="External_links" and normalize-space(.)="External links"]]//following-sibling::ul//li/a/@href').extract()
    
    ## Other_information
    #   <h3><span class="mw-headline" id="Other_information">Other information</span></h3>
    #   <ul>
    #   <li><a rel="nofollow" class="external text" href="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32003R1177:EN:NOT">Regulation (EC) No 1177/2003</a> of 16 June 2003 concerning Community statistics on income and living conditions (EU-SILC)</li>
    #   <li><a rel="nofollow" class="external text" href="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32005R1553:EN:NOT">Regulation (EC) No 1553/2005</a> of 7 September 2005 amending Regulation 1177/2003 concerning Community statistics on income and living conditions (EU-SILC)</li>
    #   <li><a rel="nofollow" class="external text" href="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32006R1791:EN:NOT">Regulation (EC) No 1791/2006</a> of 20 November 2006 adapting certain Regulations and Decisions in the fields of ... statistics, ..., by reason of the accession of Bulgaria and Romania</li>
    #   </ul>
    #   <h2><span class="mw-headline" id="External_links">External links</span></h2>
    # running:
    #       urls=response.xpath(ARTICLE_PATHS['Other_information']).extract()
    # will return: 
    #   urls = ['http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32003R1177:EN:NOT',
    #        'http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32005R1553:EN:NOT',
    #        'http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32006R1791:EN:NOT']
    
    @classmethod
    def runtest(cls, **kwargs):
        print('\n{}: Class test %s for testing item ArticleItem of items.py' % cls.__name__)
        time.sleep(0.5) 
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        unittest.TextTestRunner(verbosity=kwargs.pop('verbosity',2)).run(suite)
        return
    
#%%
# ArticleItemLoaderTestCase
class ArticleItemLoaderTestCase(unittest.TestCase):
   
    def test01_constructor(self):
        l = items.ArticleItemLoader()
        self.assertEqual(l.selector, None)

#%%
# GlossaryItemTestCase case of GlossaryItem
class GlossaryItemTestCase(unittest.TestCase):
 
    # Example: http://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Equivalised_disposable_income
    #
    # One can launch:
    # scrapy shell 'http://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Equivalised_disposable_income'
    
     
    ## Title
    #   <title>Glossary:Equivalised disposable income - Statistics Explained</title>
    # or
    #   <h1 id="firstHeading" class="firstHeading">Income distribution statistics</h1>
    # running:
    #       title=xpath(GLOSSARY_PATHS['Title']).extract_first().replace('Glossary:','').replace(' - Statistics Explained','')
    # will return: 
    #   title = 'Equivalised disposable income'
    
    ## Last_modified
    #   <div id="footer" role="contentinfo">
    #   	<ul id="f-list" class="list-inline">
    #		<li id="lastmod"> This page was last modified on 6 February 2014, at 09:25.</li>
    #        <!-- ... -->
    #   	</ul>
    #   </div>
    # running:
    #       txt=response.xpath(GLOSSARY_PATHS['Last_modified']).extract()
    # will return: 
    #   txt = [' This page was last modified on 6 February 2014, at 09:25.']
    # then one will have to run:
    #       import datefinder 
    #       [d for d in datefinder.find_dates(txt)][0]
    # so as to retrieve the (formatted) date-time (e.g.: datetime.datetime(2014, 2, 6, 19, 25))
    
    ## Categories
    #   <div id="mw-normal-catlinks" class="mw-normal-catlinks">
    #   <a href="/eurostat/statistics-explained/index.php/Special:Categories" title="Special:Categories">Categories</a>: 
    #   <ul>
    #   <li><a href="/eurostat/statistics-explained/index.php/Category:Glossary" title="Category:Glossary">Glossary</a></li>
    #   <li><a href="/eurostat/statistics-explained/index.php/Category:Living_conditions_glossary" title="Category:Living conditions glossary">Living conditions glossary</a></li>
    #   <li><a href="/eurostat/statistics-explained/index.php/Category:Statistical_indicator" title="Category:Statistical indicator">Statistical indicator</a></li>
    #   </ul>
    #   </div>
    # running:
    #       urls=response.xpath(GLOSSARY_PATHS['Categories']).extract()
    # will return: 
    #   urls = ['/eurostat/statistics-explained/index.php/Category:Household_income,_expenditure_and_debt',
    #           '/eurostat/statistics-explained/index.php/Category:Living_conditions',
    #           '/eurostat/statistics-explained/index.php/Category:Statistical_article',
    #           '/eurostat/statistics-explained/index.php/Category:Multilingual']
        
    ## Text:
    #    <div id="mw-content-text" lang="en" dir="ltr" class="mw-content-ltr">
    #   <p>The <b>equivalised disposable income</b> is the total income of a household, child tax and other deductions, that is available for spending or saving, divided by the number of household members converted into equalised adults; household members are equalised or made equivalent by weighting each according to their age, using the so-called modified <a href="/eurostat/statistics-explained/index.php/Glossary:OECD" title="Glossary:OECD" class="mw-redirect">OECD</a> equivalence scale.
    #   </p><p>The equivalised disposable income is calculated in three steps:
    #   </p>
    #   <ul>
    #   <li>all monetary incomes received from any source by each member of a household are added up; these include income from work, investment and social benefits, plus any other household income; taxes and social contributions that have been paid, are deducted from this sum;</li>
    #   <li>in order to reflect differences in a household's size and composition, the total (net) household income is divided by the number of 'equivalent adults’, using a standard (equivalence) scale: the modified OECD scale; this scale gives a weight to all members of the household (and then adds these up to arrive at the <b>equivalised household size</b>):</li>
    #   </ul>
    #   <dl>
    #   <dd><ul>
    #   <li> 1.0 to the first adult;</li>
    #   <li> 0.5 to the second and each subsequent person aged 14 and over; </li>
    #   <li> 0.3 to each child aged under 14.</li>
    #   </ul>
    #   </dd>
    #   </dl>
    #   <ul>
    #   <li>finally, the resulting figure is called the equivalised disposable income and is attributed equally to each member of the household.</li>
    #   </ul>
    #   <p>For poverty indicators, the equivalised disposable income is calculated from the total disposable income of each household divided by the equivalised household size. The income reference period is a fixed 12-month period (such as the previous calendar or tax year) for all countries except UK for which the income reference period is the current year and Ireland (IE) for which the survey is continuous and income is collected for the last twelve months.
    #   </p>
    #   <h2><span class="mw-headline" id="Related_concepts">Related concepts</span></h2>
    # running:
    #       text=response.xpath(GLOSSARY_PATHS['Text']).extract()
    # will return: 
    #   text = ['<p>The <b>equivalised disposable income</b> is the total income of a household, child tax and other deductions, that is available for spending or saving, divided by the number of household members converted into equalised adults; household members are equalise d or made equivalent by weighting each according to their age, using the so-called modified <a href="/eurostat/statistics-explained /index.php/Glossary:OECD" title="Glossary:OECD" class="mw-redirect">OECD</a> equivalence scale.\n</p>',
    #           '<p>The equivalised disposable income is calculated in three steps:\n</p>',
    #           "<ul>\n<li>all monetary incomes received from any source by each member of a household are added up; these include income from work, investment and social benefits, plus any other household income; taxes and social contributions that have been paid, are deducted from this sum;\n</li>\n<li>in order to reflect differences in a household's size and composition, the total (net) household income is divided by the number of 'equivalent adults’, using a standard (equivalence) scale: the modified OECD scale; this scale gives a weight to all members of the household (and then adds these up to arrive at the <b>equivalised household size</b>):\n</li>\n</ul>",
    #           '<dl>\n<dd><ul>\n<li> 1.0 to the first adult;\n</li>\n<li> 0.5 to the second and each subsequent person aged 14 and over; \n</li>\n<li> 0.3 to each child aged under 14.\n</li>\n</ul>\n</dd>\n</dl>',
    #           '<ul>\n<li>finally, the resulting figure is called the equivalised disposable income and is attributed equally to each member of the household.\n</li>\n</ul>',
    #           '<p>For poverty indicators, the equivalised disposable income is calculated from the total disposable income of each household divided by the equivalised household size. The income reference period is a fixed 12-month period (such as the previous calendar or tax year) for all countries except UK for which the income reference period is the current year and Ireland (IE) for which the survey is continuous and income is collected for the last twelve months.\n</p>'
    #           ]
    #       import bleach
    #       # http://bleach.readthedocs.io/en/latest/clean.html
    #       from bs4 import BeautifulSoup
    #       soup = BeautifulSoup(' '.join(text))
    #       text = bleach.clean(soup,tags=[],strip=True).replace('\n','') # ! note that I tried to use re:replace in xpath: no success...
    
    ## Further_information
    #   <h2><span class="mw-headline" id="Further_information">Further information</span></h2>
    #   <ul>
    #   <li><a rel="nofollow" class="external text" href="http://ec.europa.eu/eurostat/product?code=KS-RA-12-013&amp;language=en">The European Union Labour Force Survey: main characteristics of the national surveys</a></li>
    #   </ul>
    #   <h2><span class="mw-headline" id="Related_concepts">Related concepts</span></h2>
    # running:
    #       urls=response.xpath(GLOSSARY_PATHS['Further_information']).extract()
    # will return: 
    #   urls = []
    
    ## Related_concepts
    #   <h2><span class="mw-headline" id="Related_concepts">Related concepts</span></h2>
    #   <ul>
    #   <li><a href="/eurostat/statistics-explained/index.php/Glossary:At-risk-of-poverty_rate" title="Glossary:At-risk-of-poverty rate">At-risk-of-poverty rate</a></li>
    #   <li><a href="/eurostat/statistics-explained/index.php/Glossary:Income_quintile_share_ratio" title="Glossary:Income quintile share ratio">Income quintile share ratio (S80/S20)</a> </li>
    #   <li><a href="/eurostat/statistics-explained/index.php/Glossary:Relative_median_at-risk-of-poverty_gap" title="Glossary:Relative median at-risk-of-poverty gap">Relative median at-risk-of-poverty gap</a> </li>
    #   <li><a href="/eurostat/statistics-explained/index.php/Glossary:Relative_median_income_ratio" title="Glossary:Relative median income ratio">Relative median income ratio</a></li>
    #   </ul>
    #   <h2><span class="mw-headline" id="Statistical_data">Statistical data</span></h2>
    # running:
    #       urls=response.xpath(GLOSSARY_PATHS['Related_concepts'])
    # will return: 
    #   urls = ['/eurostat/statistics-explained/index.php/Glossary:At-risk-of-poverty_rate',
    #           '/eurostat/statistics-explained/index.php/Glossary:Income_quintile_share_ratio',
    #           '/eurostat/statistics-explained/index.php/Glossary:Relative_median_at-risk-of-poverty_gap',
    #           '/eurostat/statistics-explained/index.php/Glossary:Relative_median_income_ratio']
    #       [url.rsplit('/', 1)[-1].replace('%s:' % settings.GLOSSARY_KEY,'') for url in urls]
    # out = ['At-risk-of-poverty_rate',
    #       'Income_quintile_share_ratio',
    #       'Relative_median_at-risk-of-poverty_gap',
    #       'Relative_median_income_ratio']
    
    ## Additional urls in the text:
    #   response.xpath('//div[@id="bodyContent"]//div[@id="mw-content-text"]/p/a[contains(@href,"Glossary")]/@href').extract()
    # out = ['/eurostat/statistics-explained/index.php/Glossary:OECD']
    
    ## Statistical_data
    #   <h2><span class="mw-headline" id="Statistical_data">Statistical data</span></h2>
    #   <ul>
    #   <li><a href="/eurostat/statistics-explained/index.php/Income_distribution_statistics" title="Income distribution statistics">Income distribution statistics</a>
    #   </li>
    #   </ul>
    # running:
    #       urls=response.xpath(GLOSSARY_PATHS['Related_concepts'])
    # will return: 
    #   urls = ['/eurostat/statistics-explained/index.php/Income_distribution_statistics']    
    
    ## Categories extraction
    #   urls=response.xpath('//div[@id="catlinks"]//div[@id="mw-normal-catlinks"]//following-sibling::ul[1]/li/a/@href').extract()
    # out = ['/eurostat/statistics-explained/index.php/Category:Glossary',
    #       '/eurostat/statistics-explained/index.php/Category:Living_conditions_glossary',
    #       '/eurostat/statistics-explained/index.php/Category:Statistical_indicator']
    # [url.rsplit('/', 1)[-1].replace('%s:' % settings.CATEGORY_KEY,'') for url in urls]
    # out = ['Glossary', 'Living_conditions_glossary', 'Statistical_indicator']    
    pass



