# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import os, sys, re#analysis:ignore

import scrapy 
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, MapCompose, Join, TakeFirst, Identity
from scrapy.item import DictItem, Field

from warnings import warn#analysis:ignore
from collections import defaultdict

import time

try:
    from datetime import datetime
except (ModuleNotFoundError,ImportError):
    def _now():
        return time.asctime()
else:
    def _now():
        return datetime.now.isoformat()

try:
    from datefinder import find_dates as _find_dates
except (ModuleNotFoundError,ImportError):
    def _find_dates(arg): 
        return arg

try:
    from unicode import strip as _strip
except (ModuleNotFoundError,ImportError):
    def _strip(arg): 
        try:    return arg.strip(' \r\t\n')
        except: return arg

try:
    from scrapy.utils.markup import remove_tags as _remove_tags
except ImportError:
    try:
        from w3lib.html import remove_tags as _remove_tags
    except (ModuleNotFoundError,ImportError):
        def _remove_tags(arg): 
            start = arg.find('<')
            while start != -1:
                end = arg.find('>')
                arg = _strip(arg[:start]) + ' ' + _strip(arg[end + 1:])
                start = arg.find('<')
            return arg

from . import essError, essWarning#analysis:ignore 

#==============================================================================
# GLOBAL VARIABLES
#==============================================================================

GLOSSARY_KEY        = 'Glossary'
CATEGORY_KEY        = 'Category'
ARTICLE_KEY         = ''
THEME_KEY           = ''

ARTICLE_FIELDS      = ['Title', 'Last_modified', 'Categories', 'Hidden_categories',
                       'Source_datasets', 'See_also', 'Publications', 'Main_tables', 
                       'Database', 'Dedicated_section', 'Metadata',
                       'Other_information', 'External_links']
ARTICLE_PATHS       = dict.fromkeys(ARTICLE_FIELDS)
ARTICLE_PROCESSORS  = dict.fromkeys(ARTICLE_FIELDS)

GLOSSARY_FIELDS     = ['Title', 'Last_modified', 'Categories', 'Text', 
                       'Further_information', 'Related_concepts', 'Statistical_data']
GLOSSARY_PATHS      = dict.fromkeys(GLOSSARY_FIELDS)
GLOSSARY_PROCESSORS = dict.fromkeys(GLOSSARY_FIELDS)

CATEGORY_FIELDS     = []
CATEGORY_PATHS      = {}
CATEGORY_PROCESSORS = {}

SE_FIELDS           = {GLOSSARY_KEY: GLOSSARY_FIELDS,
                       CATEGORY_KEY: CATEGORY_FIELDS,
                       ARTICLE_KEY: ARTICLE_FIELDS}

#==============================================================================
# GLOBAL CLASSES/METHODS/
#==============================================================================

_clean_text                  = Compose(MapCompose(lambda v: v.strip()), Join())   
_to_int                      = Compose(TakeFirst(), int)
_default_input_processor     = MapCompose(_strip)
_default_output_processor    = Identity()

class xpath():
    """Class providing with the main (static) method (so-called 'xpath.create' 
    function used to "automatically" generate most of the rules that are needed
    to extract structured contents from webpage. 
    """

    @staticmethod
    def create(node=None, tag=None, first=None, last=None, identifier=None, 
               parent=None, preceding_sibling=None, preceding=None, ancestor=None,
               child=None, following_sibling=None, following=None, descendant=None,
               sep='/'):
        """Static method for generating generic xpath based on simple rules.
        
            >>> path = xpath.create(node, tag, first, last, identifier, 
                                    parent, preceding_sibling, preceding, ancestor,
                                    child, following_sibling, following, descendant, sep)     
        Arguments
        ---------
        node : str
            main (starting) node; default: None.
        tag : str               
            ending tag; default: None.
        first : str               
            tag/anchor "childing" the part to extract; default: None.
        last : str               
            tag/anchor parenting  the part to extract; default: None.
        identifier : str               
            identifier (=condition) for the (FIRST,LAST) anchors; default: None.
        parent : str               
            parent axe: True (simple '/' or '//' relation) or expression of the 
            relation; default: None. 
        preceding_sibling : str               
            preceding-sibling axe: True or expression of the relation (used with 
            "preceding-sibling" keyword); default: None.
        preceding : str               
            preceding axe: True or expression of the relation (used with "preceding" 
            keyword); default: None.
        ancestor : str               
            ancestor axe: True or expression of the relation (used with "ancestor" 
            keyword); default: None.
        child : str               
            child axe: True (simple '/' or '//' relation) or expression of the 
            relation; default: None.  
        following_sibling : str               
            following-sibling axe: True or expression of the relation (used with 
            "following-sibling" keyword); default: None.
        following : str               
            following axe: True or expression of the relation (used with "following" 
            keyword); default: None.
        descendant : str               
            descendant axe: True or expression of the relation (used with "descendant" 
            keyword); default: None.
        sep:
            ; default: '/'.
            
        Returns
        -------
        path : str
            `xpath` formatted path to be used so as to extract a specific field 
            from a webpage.
        """
        ## default settings
        if last not in (None,'') and all([kw in (None,False,'') for kw in [preceding_sibling, preceding, ancestor, parent]]):
            #warn(essWarning("Parameter PRECEDING set to True with LAST"))
            preceding=True
        if first not in (None,'') and all([kw in (None,False,'') for kw in [following_sibling, following, child, descendant]]):
            #warn(essWarning("Parameter CHILD set to True with FIRST"))
            child=True
        ## check
        if sum([kw not in ('', None) for kw in [preceding_sibling, preceding, ancestor, parent]]) > 1:
            raise essError("Incompatible keyword parameters (PRECEDING, PRECEDING_SIBLING, ANCESTOR, PARENT)")        
        elif sum([kw not in ('', None) for kw in [following_sibling, following, child, descendant]]) > 1:
            raise essError("Incompatible keyword parameters (FOLLOWING, FOLLOWING_SIBLING, DESCENDANT, CHILD)")        
        if sep not in (None,''):                    SEP=sep
        else:                                       SEP='/'
        PARENTSEP = SEP
        if preceding_sibling in ('/', '//'):        preceding_sibling, PARENTSEP = True, preceding_sibling
        elif preceding in ('/', '//'):              preceding, PARENTSEP = True, preceding
        elif ancestor in ('/', '//'):               ancestor, PARENTSEP = True, ancestor
        elif parent in ('/', '//'):                 parent, PARENTSEP = True, parent
        CHILDSEP = SEP
        if following_sibling in ('/', '//'):        following_sibling, CHILDSEP = True, following_sibling
        elif following in ('/', '//'):              following, CHILDSEP = True, following
        elif descendant in ('/', '//'):             descendant, CHILDSEP = True, descendant
        elif child in ('/', '//'):                  child, CHILDSEP = True, child
        if not (last in (None,'') or all([kw in (None,True,'') for kw in [preceding_sibling, preceding, parent, ancestor]])):
            raise essError("Instructions for (PRECEDING, PRECEDING_SIBLING, PARENT, ANCESTOR) incompatible with keyword parameter LAST")
        elif last in (None,'') and all([kw in (None,True,'') for kw in [preceding_sibling, preceding, parent, ancestor]]):
            #esScrape("Instructions for (PRECEDING, PRECEDING_SIBLING, ANCESTOR, PARENT) ignored in absence of parameter LAST")
            preceding_sibling = preceding = parent = ancestor = None
        if not (first in (None,'') or all([kw in (None,True,'') for kw in [following_sibling, following, child, descendant]])):
            raise essError("Instructions for (FOLLOWING, FOLLOWING_SIBLING, CHILD, DESCENDANT) incompatible with keyword parameter FIRST")
        elif first in (None,'') and all([kw in (None,True,'') for kw in [following_sibling, following, child, descendant]]):
            # this may ignored in case the default setting on first above is actually run
            #esScrape("Parameters (FOLLOWING, FOLLOWING_SIBLING, DESCENDANT, CHILD) ignored in absence of parameter FIRST")
            following_sibling = following = child = descendant = None
        ## set
        prec, follow = '', ''
        if preceding_sibling not in ('', None):    prec, parent = 'preceding-sibling::', preceding_sibling
        elif preceding not in ('', None):          prec, parent = 'preceding::', preceding
        elif ancestor not in ('', None):           prec, parent = 'ancestor::', ancestor
        elif parent not in ('', None):             prec         = 'parent::' # parent unchanged
        else:                                      parent = None 
        if following_sibling not in ('', None):    follow, child = 'following-sibling::', following_sibling
        elif following not in ('', None):          follow, child = 'following::', following
        elif descendant not in ('', None):         follow, child = 'descendant::', descendant
        elif child not in ('', None):              follow        = '' # child unchanged
        else:                                      child = None
        ## further check
        if not node in (None,'') and not node.startswith('/'):          
            node = '//%s' % node
        #if not tag in ('',None) and not tag.startswith('/'):     
        #    tag = '//%s' %tag
        if not identifier in (None,'') and not identifier.startswith('['):     
            identifier = '[%s]' % identifier
        ## run
        # initialise xrule
        xrule=''
        if not last in (None,''):
            if not identifier in (None,''):
                last = '%s%s' % (last,identifier)
            if not (first is None or (parent in (None,'') or isinstance(parent,bool))):
                if follow=='' and not last.startswith('/'):     last = '*[%s%s]' % (PARENTSEP,last)
                else:                                           last = '*[%s]' % last  
            elif not first is None:
                if follow=='' and not last.startswith('/'):     last = '%s%s' % (PARENTSEP,last)
                # else:                                         do nothing! 
            elif not node in (None,''):
                last = '%s%s' % (SEP, last) # not PARENTSEP!
            else:
                last = '//%s' % last # '%s%s' % (SEP, last)
            if prec!='' and parent not in ('', None):
                last = '%s%s%s' % (last, PARENTSEP, prec)
            elif not child in (None,True,''): 
                last = '%s%s' % (last, PARENTSEP)
        elif not (parent in (None, '') or isinstance(parent,bool)): #not all([kw in (True, '', None) for kw in [preceding_sibling, preceding, parent, ancestor]]):
            last = '%s%s' % (prec, parent)        
            if not identifier in (None,''):
                last = '%s%s' % (last,identifier)
            if not first is None :
                last = '*[%s]' % last  
        if not first in (None,''):
            if not identifier in (None,''):
                first = '%s%s' % (first,identifier)
            if not (last is None or (child in (None, '') or isinstance(child,bool))):
                if prec=='' and not first.startswith('/'):      first = '*[%s%s]' % (CHILDSEP,first)
                else:                                           first = '*[%s]' % first  
            elif not last is None:
                if prec=='' and not first.startswith('/'):      first = '%s%s' % (CHILDSEP,first)
                elif node in (None,''):                         first = '//%s' % first
            elif not node in (None,''):
                first = '%s%s' % (SEP, first)
            else:
                first = '//%s' % first
            if follow!='' and child not in ('', None):
                first = '%s%s%s' % (first, CHILDSEP, follow)
            elif not (parent in (None,'') or isinstance(parent,bool)): 
                first = '%s%s' % (first, CHILDSEP)
        elif not (child in (None, '') or isinstance(child,bool)): #not all([kw in (True, '', None) for kw in [following_sibling, following, child, descendant]]):
            first = '%s%s' % (follow, child)
            if not identifier in (None,''):
                first = '%s%s' % (first,identifier)
        if not (first in (None,'') or parent in (None,'') or isinstance(parent,bool)):
            if last in (None,'') and follow!='':
                xrule = '%s%s' % (xrule, first)
            elif last in (None,''):
                xrule = '%s%s*' % (xrule, first)
            elif last.startswith('/'):
                xrule = '%s%s*[%s]' % (xrule, first, last)
            else:
                xrule = '%s%s%s' % (xrule, first, last)
        elif not (last in (None,'') or child in (None,'') or isinstance(child,bool)):
            if first in (None,'') and prec!='':
                xrule = '%s%s' % (xrule, last)
            elif first in (None,''):
                xrule = '%s%s*' % (xrule, last)
            elif first.startswith('/'):
                xrule = '%s%s*[%s]' % (xrule, last, first)
            else:
                xrule = '%s%s%s' % (xrule, last, first)
        elif not all([kw in (None,False,'') for kw in [preceding_sibling, preceding, ancestor]]):
             xrule = '%s%s%s' % (xrule, last or '', first or ('*' if tag in ('',None) else '')) 
        elif not all([kw in (None,False,'') for kw in [following_sibling, following, descendant]]):
             xrule = '%s%s%s' % (xrule, first or '', last or ('*' if tag in ('',None) else '')) 
        else:
             xrule = '%s%s%s' % (xrule, last or '', first or '')  
        if not node in (None,''):
            if not (node.endswith('/') or node.endswith('/') or xrule.startswith('/')) or xrule.startswith('*'):      
                xrule = '%s%s%s' % (node, SEP, xrule)
            elif node.endswith('::') and xrule.startswith('/') and not xrule.startswith('*'):
                xrule = '%s*%s' % (node, xrule)
            elif not (node.endswith('::') or node.endswith('/') or xrule.startswith('/') or xrule.startswith('*')):
                xrule = '%s%s*%s' % (node, SEP, xrule)
            else:                           
                xrule = '%s%s' % (node, xrule)   
        if not tag in ('',None):
            if not (xrule.endswith('::') or xrule.endswith('/') or tag.startswith('/') or tag.startswith('*')):
                xrule = '%s%s%s' % (xrule, SEP, tag)
            elif xrule.endswith('::') and tag.startswith('/') and not tag.startswith('*'):
                xrule = '%s*%s' % (xrule, tag)
            elif not (xrule.endswith('::') or xrule.endswith('/') or tag.startswith('/') or tag.startswith('*')):
                xrule = '%s%s*%s' % (xrule, SEP, tag)
            else:                           
                xrule = '%s%s' % (xrule, tag)   
        return xrule

#==============================================================================
# GLOBAL VARIABLES SETTING
#==============================================================================

## Title
ARTICLE_PATHS['Title'] =                                    \
    xpath.create(first='h1[@id="firstHeading"]', 
                 tag='text()[normalize-space(.)]')
# that is:
#   '//h1[@id="firstHeading"]/text()[normalize-space(.)]'
# one could also try: 
#   __xpath.create(first='title', tag='text()[normalize-space(.)]')
ARTICLE_PROCESSORS['Title'] =                               \
    {'in':  TakeFirst(),
     'out': _default_output_processor}

## Last_modified
ARTICLE_PATHS['Last_modified'] =                            \
    xpath.create(node='div[@id="footer"]',                            
                 first='li[@id="lastmod"]',  
                 tag='text()',
                 sep='//')
# that is actually:    
#   '//div[@id="footer"]//li[@id="lastmod"]//text()'
ARTICLE_PROCESSORS['Last_modified'] =                       \
    {'in':  Compose(_remove_tags, TakeFirst()),
     'out': _find_dates} 

## Categories
ARTICLE_PATHS['Categories'] =                               \
    xpath.create(first='div',                                    
                 tag='a/@href',                                
                 identifier='@id="mw-normal-catlinks"',  
                 ancestor='*[starts-with(name(),"div")][1]',                           
                 descendant=True,
                 sep='//')
# that is:    
#   '//div[@id="mw-normal-catlinks"]//descendant::*[ancestor::*[starts-with(name(),"div")][1][@id="mw-normal-catlinks"]]//a/@href'
ARTICLE_PROCESSORS['Categories'] =                          \
    {'in':  _default_input_processor,
     'out': _default_output_processor}

## Hidden_categories
ARTICLE_PATHS['Hidden_categories'] =                        \
    xpath.create(first='div',                                    
                 tag='a/@href',                                
                 identifier='@id="mw-hidden-catlinks"',  
                 ancestor='*[starts-with(name(),"div")][1]',                           
                 descendant=True,
                 sep='//')
# that is:    
#   '//div[@id="mw-hidden-catlinks"]//descendant::*[ancestor::*[starts-with(name(),"div")][1][@id="mw-hidden-catlinks"]]//a/@href'
ARTICLE_PROCESSORS['Hidden_categories'] =                   \
    {'in':  _default_input_processor,
     'out': _default_output_processor}
    
## Source_datasets:
ARTICLE_PATHS['Source_datasets'] =                          \
    xpath.create(node='div[@class="thumb tright"]',
                 first='i[contains(text(),"Source")]',                                    
                 tag='a[1]/@href',                                
                 following_sibling=True,                           
                 sep='//')
# that is:    
#   '//div[@class="thumb tright"]//i[contains(text(),"Source")]//following-sibling::a[1]/@href'
# (also accept: '//div[@class="thumb tright"]//i[contains(text(),"Source")]/following-sibling::a[1]/@href')
ARTICLE_PROCESSORS['Source_datasets'] =                     \
    {'in':  _default_input_processor,
     'out': _default_output_processor}

## See_also:
ARTICLE_PATHS['See_also'] =                                 \
    xpath.create(first='h2',
                 tag='a/@href',
                 identifier='span[@id="See_also"]',
                 #identifier='span[@id="See_also" and normalize-space(.)="See also"]',
                 following_sibling=True,
                 preceding_sibling='*[starts-with(name(),"h")][1]',
                 #preceding_sibling='h2[span[@id="Further_Eurostat_information"]]',
                 sep='//')
# that is:    
#   '//h2[span[@id="See_also"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="See_also"]]]//a/@href'
# note that this will work as well:
#   '//h2[span[@id="See_also" and normalize-space(.)="See also"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1]/span[@id="See_also" and normalize-space(.)="See also"]]//a/@href'
ARTICLE_PROCESSORS['See_also'] =                            \
    {'in':  _default_input_processor,
     'out': _default_output_processor}

## Publications:
ARTICLE_PATHS['Publications'] =                             \
    xpath.create(first='h3',
                 tag='li/a/@href',
                 identifier='span[@id="Publications"]',
                 #identifier='span[@id="Publications" and normalize-space(.)="Publications"]',
                 following_sibling=True,
                 preceding_sibling='*[starts-with(name(),"h")][1]',
                 #preceding_sibling='h3[span[@id="Main_tables"]]'
                 sep='//')
# that is:    
#   '//h3[span[@id="Publications"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Publications"]]]//li/a/@href'
# note that this will work as well:    
#   '//h3[span[@id="Publications" and normalize-space(.)="Publications"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1]/span[@id="Publications" and normalize-space(.)="Publications"]]//li/a/@href'
ARTICLE_PROCESSORS['Publications'] =                        \
    {'in':  _default_input_processor,
     'out': _default_output_processor}
   
## Main_tables
ARTICLE_PATHS['Main_tables'] =                              \
    xpath.create(first='h3',
                 tag='li/a/@href',
                 identifier='span[@id="Main_tables"]',
                 #identifier='span[@id="Main_tables" and normalize-space(.)="Main tables"]',
                 following_sibling=True,
                 preceding_sibling='*[starts-with(name(),"h")][1]',
                 #preceding_sibling='h3[span[@id="Database"]]'
                 sep='//')
# that is:    
#   '//h3[span[@id="Main_tables"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Main_tables"]]]//li/a/@href'
# note that this will work as well:
#   '//h3[span[@id="Main_tables" and normalize-space(.)="Main tables"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1]/span[@id="Main_tables" and normalize-space(.)="Main tables"]]//li/a/@href'
ARTICLE_PROCESSORS['Main_tables'] =                         \
    {'in':  _default_input_processor,
     'out': _default_output_processor}
    
## Database     
ARTICLE_PATHS['Database'] =                                 \
    xpath.create(first='h3',
                 tag='li/a/@href',
                 identifier='span[@id="Database"]',
                 #identifier='span[@id="Database" and normalize-space(.)="Database"]',
                 following_sibling=True,
                 preceding_sibling='*[starts-with(name(),"h")][1]',
                 #preceding_sibling='h3[span[@id="Dedicated_section"]]'
                 sep='//')
# that is:    
#   '//h3[span[@id="Database"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Database"]]]//li/a/@href'
ARTICLE_PROCESSORS['Database'] =                            \
    {'in':  _default_input_processor,
     'out': _default_output_processor}

## Dedicated_section
ARTICLE_PATHS['Dedicated_section'] =                        \
    xpath.create(first='h3',
                 tag='li/a/@href',
                 identifier='span[@id="Dedicated_section"]',
                 following_sibling=True,
                 preceding_sibling='*[starts-with(name(),"h")][1]',
                 #preceding_sibling='h2[span[@id="Methodology_.2F_Metadata"]]'
                 sep='//')
# that is:    
#   '//h3[span[@id="Dedicated_section"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Dedicated_section"]]]//li/a/@href'
# note that this will work as well:
#   '//h3[span[@id="Dedicated_section" and normalize-space(.)="Dedicated section"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1]/span[@id="Dedicated_section" and normalize-space(.)="Dedicated section"]]//li/a/@href'
ARTICLE_PROCESSORS['Dedicated_section'] =                   \
    {'in':  _default_input_processor,
     'out': _default_output_processor}

## Metadata
ARTICLE_PATHS['Metadata'] =                                 \
    xpath.create(first='h3',
                 tag='li/a/@href',
                 identifier='span[@id="Methodology_.2F_Metadata"]',
                 # identifier='span[@id="Methodology_.2F_Metadata" and normalize-space(.)="Methodology / Metadata"]',    
                 following_sibling=True,
                 preceding_sibling='*[starts-with(name(),"h")][1]',
                 #preceding_sibling='h2[span[@id="Source_data_for_tables_and_figures_.28MS_Excel.29"]]'
                 sep='//')
# that is:    
#   '//h3[span[@id="Methodology_.2F_Metadata"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Methodology_.2F_Metadata"]]]//li/a/@href'
# note that this will work as well:
#   '//h3[span[@id="Methodology_.2F_Metadata"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1]/span[@id="Methodology_.2F_Metadata"]]//li/a/@href'
ARTICLE_PROCESSORS['Metadata'] =                            \
    {'in':  _default_input_processor,
     'out': _default_output_processor}

## External_links: 
ARTICLE_PATHS['External_links'] =                           \
    xpath.create(first='h2',
                 tag='li/a/@href',
                 identifier='span[@id="External_links"]',
                 #identifier='span[@id="External_links" and normalize-space(.)="External links"]',
                 following_sibling=True,
                 preceding_sibling='*[starts-with(name(),"h")][1]',
                 sep='//')
# that is:    
#   '//h2[span[@id="External_links"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="External_links"]]]//li/a/@href'
# note that this will work as well:
#   '//h2[span[@id="External_links" and normalize-space(.)="External links"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1]/span[@id="External_links" and normalize-space(.)="External links"]]//li/a/@href'
ARTICLE_PROCESSORS['External_links'] =                      \
    {'in':  _default_input_processor,
     'out': _default_output_processor}

## Other_information
ARTICLE_PATHS['Other_information'] =                        \
    xpath.create(first='h3',
                 tag='li/a/@href',
                 identifier='span[@id="Other_information"]',
                 # identifier='span[@id="Other_information" and normalize-space(.)="Other information"]',
                 following_sibling=True,
                 preceding_sibling='*[starts-with(name(),"h")][1]',
                 #preceding_sibling='h2[span[@id="External_links" and normalize-space(.)="External links"]]'
                 sep='//')
# that is:    
#   '//h3[span[@id="Other_information"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Other_information"]]]//li/a/@href'
# note that this will work as well:
#   '//h3[span[@id="Other_information"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1]/span[@id="Other_information]]//li/a/@href'
ARTICLE_PROCESSORS['Other_information'] =                    \
    {'in':  _default_input_processor,
     'out': _default_output_processor}

#%%
## Glossary pages
 
# Example: http://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Equivalised_disposable_income
#
# One can launch:
# scrapy shell 'http://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Equivalised_disposable_income'

 
## Title
GLOSSARY_PATHS['Title'] =                                   \
    xpath.create(first='h1[@id="firstHeading"]', 
                 tag='text()[normalize-space(.)]')
# that is:
#   '//h1[@id="firstHeading"]/text()[normalize-space(.)]'
GLOSSARY_PROCESSORS['Title'] =                              \
    {'in':  TakeFirst(),
     'out': _default_output_processor} 

## Last_modified
GLOSSARY_PATHS['Last_modified'] =                           \
    xpath.create(node='div[@id="footer"]',                            
                 first='li[@id="lastmod"]',  
                 tag='text()',
                 sep='//')
# that is actually:    
#   '//div[@id="footer"]//li[@id="lastmod"]//text()'
GLOSSARY_PROCESSORS['Last_modified'] =                      \
    {'in':  Compose(_remove_tags, TakeFirst()),
     'out': _find_dates} 

## Categories
GLOSSARY_PATHS['Categories'] =                              \
    xpath.create(first='div',                                    
                 tag='a/@href',                                
                 identifier='@id="mw-normal-catlinks"',  
                 ancestor='*[starts-with(name(),"div")][1]',                           
                 descendant=True,
                 sep='//')
# that is actually:   
#   '//div[@id="mw-normal-catlinks"]//descendant::*[ancestor::*[starts-with(name(),"div")][1][@id="mw-normal-catlinks"]]//a/@href'
GLOSSARY_PROCESSORS['Categories'] =                         \
    {'in':  _default_input_processor,
     'out': _default_output_processor}
    
## Text:
GLOSSARY_PATHS['Text'] =                                    \
    xpath.create(node='div[@id="bodyContent"]',
                 last='h2[span[@id="Related_concepts"]]',
                 child='//div[@id="mw-content-text"]',
                 preceding_sibling='/',
                 sep='//')
# that is actually:    
#   '//div[@id="bodyContent"]//h2[span[@id="Related_concepts"]]/preceding-sibling::*[//div[@id="mw-content-text"]]'
# note that this will work as well:
#   '//div[@id="bodyContent"]//h2[span[@id="Related_concepts"]]/preceding-sibling::*[//div[@id="mw-content-text"]/descendant::*]'
GLOSSARY_PROCESSORS['Text'] =                               \
    {'in':  MapCompose(_remove_tags),
     'out': Join(' ')} 

## Further_information
GLOSSARY_PATHS['Further_information'] =                     \
    xpath.create(first='h2',
                 tag='li/a/@href',
                 identifier='span[@id="Further_information"]',
                 # identifier='span[@id="Further_information" and normalize-space(.)="Further information"]',
                 following_sibling=True,
                 preceding_sibling='*[starts-with(name(),"h")][1]',
                 #preceding_sibling='h2[span[@id="Related_concepts"]]'
                 sep='//')
# that is actually:    
#   '//h2[span[@id="Further_information"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Further_information"]]]//li/a/@href'
GLOSSARY_PROCESSORS['Further_information'] =                \
    {'in':  _default_input_processor,
     'out': _default_output_processor} 

## Related_concepts
GLOSSARY_PATHS['Related_concepts'] =                        \
    xpath.create(node='div[@id="bodyContent"]',
                 tag='ul[1]/li/a/@href',
                 first='h2[span[@id="Related_concepts"]]',
                 #first='span[@id="Related_concepts" and contains(text(),"Related concepts")]',
                 last='h2[span[@id="Statistical_data"]]',
                 following_sibling=True,
                 sep='//')
# that is actually:    
#   '//div[@id="bodyContent"]//h2[span[@id="Statistical_data"]]//preceding::h2[span[@id="Related_concepts"]]//following-sibling::ul[1]/li/a/@href'
# note that this will work as well:
#   '//div[@id="bodyContent"]//h2[span[@id="Statistical_data"]]//preceding-sibling::*[//h2[span[@id="Related_concepts"]]//following-sibling::ul[1]]/li/a/@href'
# or:
#   '//div[@id="bodyContent"]//h2[span[@id="Related_concepts"]][following::h2[span[@id="Statistical_data"]]]//following-sibling::ul[1]/li/a/@href'
GLOSSARY_PROCESSORS['Related_concepts'] =                   \
    {'in':  _default_input_processor,
     'out': _default_output_processor}

## Statistical_data
GLOSSARY_PATHS['Statistical_data'] =                        \
    xpath.create(tag='ul/li/a/@href',
                 first='h2[span[@id="Statistical_data"]]',
                 #first='span[@id="Statistical_data" and contains(text(),"Statistical data")]',
                 following_sibling=True,
                 sep='//')
# that is actually:    
#   '//h2[span[@id="Statistical_data"]]//following-sibling::ul/li/a/@href'
# note that this will work as well:
#   '//h2[span[@id="Statistical_data"]]//following-sibling::*[//ul/li/a]//@href'
GLOSSARY_PROCESSORS['Statistical_data'] =                    \
    {'in':  _default_input_processor,
     'out': _default_output_processor} 

CATEGORY_PATHS      = {}

SE_PATHS            = {GLOSSARY_KEY: GLOSSARY_PATHS,
                       CATEGORY_KEY: CATEGORY_PATHS,
                       ARTICLE_KEY: ARTICLE_PATHS}

#==============================================================================
# ITEM CLASSES
#==============================================================================
   
def __base_item_class(class_name, field_names, **kwargs):
    processors, paths = kwargs.get('processors', {}), kwargs.get('paths', {})
    fields = defaultdict(Field) 
    for key in field_names:
        if processors in ({},None):
            fields[key] = scrapy.Field()
        else:
            fields[key] = scrapy.Field(
                            input_processor=processors[key]['in'],
                            output_processor=processors[key]['out']
                            )
    return type(str(class_name), (scrapy.Item,), 
                {'fields': fields, 'paths': paths, 'processors': processors}
                )

GlossaryItem = __base_item_class('GlossaryItem', GLOSSARY_FIELDS, 
                                 processors=GLOSSARY_PROCESSORS, paths=GLOSSARY_PATHS)

ArticleItem = __base_item_class('GlossaryItem', ARTICLE_FIELDS, 
                                 processors=ARTICLE_PROCESSORS, paths=ARTICLE_PATHS)

CategoryItem = __base_item_class('GlossaryItem', CATEGORY_FIELDS, 
                                 processors=CATEGORY_PROCESSORS, paths=CATEGORY_PATHS)

#from scrapy.item import BaseItem
#class _FlexibleItem(dict, BaseItem):
#   pass
#
#class __BaseItem(scrapy.Item):
#    processors, paths = {}, {}
#    _allowed_keys = []   
#    def __setitem__(self, key, value):
#        if key not in self._allowed_keys:
#            raise essError("Key %s not supported for glossary item" % key)
#        if key not in self.fields:
#            self.fields[key] = Field(
#                            input_processor=self.processors[key]['in'],
#                            output_processor=self.processors[key]['out'])
#        #super(__BaseItem,self).__setitem__(key, value)   
#        self._values[key] = value    
#class GlossaryItem(__BaseItem):
#    _allowed_keys = GLOSSARY_FIELDS
#    fields = dict.fromkeys(_allowed_keys)
#    processors = GLOSSARY_PROCESSORS
#    paths = GLOSSARY_PATHS
#class ArticleItem(__BaseItem):
#    _allowed_keys = ARTICLE_FIELDS
#    processors = ARTICLE_PROCESSORS
#    paths = ARTICLE_PATHS
#class CategoryItem(__BaseItem):
#    _allowed_keys = CATEGORY_FIELDS
#    processors = CATEGORY_PROCESSORS
#    paths = CATEGORY_PATHS

#==============================================================================
# ITEMLOADER CLASSES
#==============================================================================

class __BaseItemLoader(ItemLoader):
    default_input_processor = MapCompose(_strip)
    default_output_processor = Identity()
    
    def get_collected_values(self, field_name):
        return (self._values[field_name]
                if field_name in self._values
                else self._values.__default_factory())

    def add_fallback_xpath(self, field_name, path, *processors, **kwargs):
        if not any(self.get_collected_values(field_name)):
            self.add_xpath(field_name, path, *processors, **kwargs)
                       
class GlossaryItemLoader(__BaseItemLoader):
    def __init__(self, *args, **kwargs):
        return super(GlossaryItemLoader,self).__init__(GlossaryItem(), *args, **kwargs)

class ArticleItemLoader(__BaseItemLoader):
    def __init__(self, *args, **kwargs):
        return super(ArticleItemLoader,self).__init__(ArticleItem(), *args, **kwargs)

class CategoryItemLoader(__BaseItemLoader):
    def __init__(self, *args, **kwargs):
        return super(CategoryItemLoader,self).__init__(CategoryItem(), *args, **kwargs)

