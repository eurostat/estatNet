#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. _items.py

*credits*:      `gjacopo <jacopo.grazzini@ec.europa.eu>`_ 

*version*:      0.1
--
*since*:        Mon Dec 18 17:28:29 2017

**Usage**

    >>> from scraprostat import items

**Contents**


"""
# Models for Eurostat scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#%%
import os, sys, re#analysis:ignore

import scrapy 
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, MapCompose, Join, TakeFirst, Identity
# from scrapy.item import DictItem, Field

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

from . import scrapError, scrapWarning#analysis:ignore 
from . import settings#analysis:ignore

#%%
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
            #warn(scrapyroWarning("Parameter PRECEDING set to True with LAST"))
            preceding=True
        if first not in (None,'') and all([kw in (None,False,'') for kw in [following_sibling, following, child, descendant]]):
            #warn(scrapyroWarning("Parameter CHILD set to True with FIRST"))
            child=True
        ## check
        if sum([kw not in ('', None) for kw in [preceding_sibling, preceding, ancestor, parent]]) > 1:
            raise scrapError("Incompatible keyword parameters (PRECEDING, PRECEDING_SIBLING, ANCESTOR, PARENT)")        
        elif sum([kw not in ('', None) for kw in [following_sibling, following, child, descendant]]) > 1:
            raise scrapError("Incompatible keyword parameters (FOLLOWING, FOLLOWING_SIBLING, DESCENDANT, CHILD)")        
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
            raise scrapError("Instructions for (PRECEDING, PRECEDING_SIBLING, PARENT, ANCESTOR) incompatible with keyword parameter LAST")
        elif last in (None,'') and all([kw in (None,True,'') for kw in [preceding_sibling, preceding, parent, ancestor]]):
            #esScrape("Instructions for (PRECEDING, PRECEDING_SIBLING, ANCESTOR, PARENT) ignored in absence of parameter LAST")
            preceding_sibling = preceding = parent = ancestor = None
        if not (first in (None,'') or all([kw in (None,True,'') for kw in [following_sibling, following, child, descendant]])):
            raise scrapError("Instructions for (FOLLOWING, FOLLOWING_SIBLING, CHILD, DESCENDANT) incompatible with keyword parameter FIRST")
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

#%%
#==============================================================================
# GLOBAL VARIABLES
#==============================================================================
        
ARTICLE_FIELDS      = ['Links', 'Title', 'Last_modified', 'Language',
                       'Categories', 'Hidden_categories',
                       'Source_datasets', 'See_also', 'Publications', 'Main_tables', 
                       'Database', 'Dedicated_section', 'Metadata',
                       'Other_information', 'External_links']

GLOSSARY_FIELDS     = ['Links', 'Title', 'Last_modified', 'Language','Categories',  
                       'Text', 'Further_information', 'Related_concepts', 'Statistical_data']

CATEGORY_FIELDS     = ['Links', 'Title', 'Last_modified', 'Language','Pages']

THEME_FIELDS        = ['Links', 'Title', 'Last_modified', 'Language', 
                       'Statistical_articles', 'Topics', 'Online_publications',
                       'Overview', 'Background_articles', 'Glossary']

CONCEPT_FIELDS      = GLOSSARY_FIELDS

SE_FIELDS           = {settings.GLOSSARY_KEY:   GLOSSARY_FIELDS,
                       settings.CATEGORY_KEY:   CATEGORY_FIELDS,
                       settings.ARTICLE_KEY:    ARTICLE_FIELDS,
                       settings.THEME_KEY:      THEME_FIELDS,
                       settings.CONCEPT_KEY:      CONCEPT_FIELDS}

#%%
## definition of ARTICLE paths and processors

try:
    assert ARTICLE_PATHS
    assert not (ARTICLE_PATHS in (None,{}) or all([v in ([],'',None) for v in ARTICLE_PATHS.values()]))
except (NameError,AssertionError):
    ARTICLE_PATHS       = dict.fromkeys(ARTICLE_FIELDS)
   ## Title
    ARTICLE_PATHS['Title'] =                                    \
        xpath.create(first='h1[@id="firstHeading"]', 
                     tag='text()[normalize-space(.)]')
    # that is:
    #   '//h1[@id="firstHeading"]/text()[normalize-space(.)]'
    # one could also try: 
    #   __xpath.create(first='title', tag='text()[normalize-space(.)]')    
    ## Last_modified
    ARTICLE_PATHS['Last_modified'] =                            \
        xpath.create(node='div[@id="footer"]',                            
                     first='li[@id="lastmod"]',  
                     tag='text()',
                     sep='//')
    # that is actually:    
    #   '//div[@id="footer"]//li[@id="lastmod"]//text()'    
    ## Language
    ARTICLE_PATHS['Language'] =                                 \
        xpath.create(node='html',                            
                     tag='@lang')
    # nothing else than: '//html/@lang'
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
    ARTICLE_PATHS['Links'] = ARTICLE_PATHS['See_also']
#else:
#    warn(scrapyroWarning("Glocal variable ARTICLE_PATHS already defined"))
            
try:
    assert ARTICLE_PROCESSORS
    assert not (ARTICLE_PROCESSORS in (None,{}) or all([v in ([],'',None) for v in ARTICLE_PROCESSORS.values()]))
except (NameError,AssertionError):
    ARTICLE_PROCESSORS  = dict.fromkeys(ARTICLE_FIELDS)
    ARTICLE_PROCESSORS['Title'] =                               \
        {'in':  TakeFirst(),
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['Language'] =                            \
        {'in':  TakeFirst(),
         'out': _default_output_processor} 
    ARTICLE_PROCESSORS['Last_modified'] =                       \
        {'in':  Compose(_remove_tags, TakeFirst()),
         'out': _find_dates} 
    ARTICLE_PROCESSORS['Categories'] =                          \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['Hidden_categories'] =                   \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['Source_datasets'] =                     \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['See_also'] =                            \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['Publications'] =                        \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['Main_tables'] =                         \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['Database'] =                            \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['Dedicated_section'] =                   \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['Metadata'] =                            \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['External_links'] =                      \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['Other_information'] =                   \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    ARTICLE_PROCESSORS['Links'] = ARTICLE_PROCESSORS['See_also']
#else:
#    warn(scrapyroWarning("Glocal variable ARTICLE_PROCESSORS already defined"))        
     
#%%
## definition of GLOSSARY paths and processors

try:
    assert GLOSSARY_PATHS
    assert not (GLOSSARY_PATHS in (None,{}) or all([v in ([],'',None) for v in GLOSSARY_PATHS.values()]))
except (NameError,AssertionError):
    GLOSSARY_PATHS      = {}
    # GLOSSARY_PATHS      = dict.fromkeys(GLOSSARY_FIELDS)
    ## Title
    GLOSSARY_PATHS['Title'] =                                   \
        xpath.create(first='h1[@id="firstHeading"]', 
                     tag='text()[normalize-space(.)]')
    # that is:
    #   '//h1[@id="firstHeading"]/text()[normalize-space(.)]'    
    ## Language
    GLOSSARY_PATHS['Language'] =                                \
        xpath.create(node='html',                            
                     tag='@lang')
    # nothing else than: '//html/@lang'
    ## Last_modified
    GLOSSARY_PATHS['Last_modified'] =                           \
        xpath.create(node='div[@id="footer"]',                            
                     first='li[@id="lastmod"]',  
                     tag='text()',
                     sep='//')
    # that is actually:    
    #   '//div[@id="footer"]//li[@id="lastmod"]//text()'    
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
    GLOSSARY_PATHS['Links'] = GLOSSARY_PATHS['Related_concepts']

try:
    assert GLOSSARY_PROCESSORS
    assert not (GLOSSARY_PROCESSORS in (None,{}) or all([v in ([],'',None) for v in GLOSSARY_PROCESSORS.values()]))
except (NameError,AssertionError):
    GLOSSARY_PROCESSORS = {}
    # GLOSSARY_PROCESSORS = dict.fromkeys(GLOSSARY_FIELDS)
    GLOSSARY_PROCESSORS['Title'] =                              \
        {'in':  TakeFirst(),
         'out': _default_output_processor} 
    GLOSSARY_PROCESSORS['Language'] =                           \
        {'in':  TakeFirst(),
         'out': _default_output_processor} 
    GLOSSARY_PROCESSORS['Last_modified'] =                      \
        {'in':  Compose(_remove_tags, TakeFirst()),
         'out': _find_dates} 
    GLOSSARY_PROCESSORS['Categories'] =                         \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    GLOSSARY_PROCESSORS['Text'] =                               \
        {'in':  MapCompose(_remove_tags),
         'out': Join(' ')} 
    GLOSSARY_PROCESSORS['Further_information'] =                \
        {'in':  _default_input_processor,
         'out': _default_output_processor} 
    GLOSSARY_PROCESSORS['Related_concepts'] =                   \
        {'in':  _default_input_processor,
         'out': _default_output_processor}
    GLOSSARY_PROCESSORS['Statistical_data'] =                   \
        {'in':  _default_input_processor,
         'out': _default_output_processor} 
    GLOSSARY_PROCESSORS['Links'] = GLOSSARY_PROCESSORS['Related_concepts']
     
#%%
## definition of CATEGORY paths and processors
 
try:
    assert CATEGORY_PATHS
    assert not (CATEGORY_PATHS in (None,{}) or all([v in ([],'',None) for v in CATEGORY_PATHS.values()]))
except (NameError,AssertionError):
    CATEGORY_PATHS      = {}
    ## Title
    #    <title>Category:Living conditions glossary - Statistics Explained</title>
    #    <h1 id="firstHeading" class="firstHeading">Category:Living conditions glossary	</h1>
    CATEGORY_PATHS['Title'] =                                   \
        xpath.create(first='h1[@id="firstHeading"]', 
                     tag='text()[normalize-space(.)]')
    # that is:
    #   '//h1[@id="firstHeading"]/text()[normalize-space(.)]'    
    ## Language
    CATEGORY_PATHS['Language'] =                                \
        xpath.create(node='html',                            
                     tag='@lang')
    # nothing else than: '//html/@lang'
    ## Last_modified
    #    <div id="footer" role="contentinfo">
    #	<ul id="f-list" class="list-inline">
    #		<li id="lastmod"> This page was last modified on 12 November 2014, at 09:43.</li>
    CATEGORY_PATHS['Last_modified'] =                           \
        xpath.create(node='div[@id="footer"]',                            
                     first='li[@id="lastmod"]',  
                     tag='text()',
                     sep='//')
    # that is actually:    
    #   '//div[@id="footer"]//li[@id="lastmod"]//text()'   
    ## Pages in (sub)category
    CATEGORY_PATHS['Pages'] =                                   \
        xpath.create(first='div',                                    
                     tag='li/a/@href',                                
                     identifier='@class="mw-content-ltr"',  
                     ancestor='*[starts-with(name(),"div")][1]',                           
                     descendant=True,
                     sep='//')
    # that is actually:    
    #   '//div[@class="mw-content-ltr"]//descendant::*[ancestor::*[starts-with(name(),"div")][1][@class="mw-content-ltr"]]//li/a/@href'
    CATEGORY_PATHS['Links'] = CATEGORY_PATHS['Pages']
    
try:
    assert CATEGORY_PROCESSORS
    assert not (CATEGORY_PROCESSORS in (None,{}) or all([v in ([],'',None) for v in CATEGORY_PROCESSORS.values()]))
except (NameError,AssertionError):
    CATEGORY_PROCESSORS = {}
    CATEGORY_PROCESSORS['Title'] =                              \
        {'in':  TakeFirst(),
         'out': _default_output_processor} 
    CATEGORY_PROCESSORS['Language'] =                           \
        {'in':  TakeFirst(),
         'out': _default_output_processor} 
    CATEGORY_PROCESSORS['Last_modified'] =                      \
        {'in':  Compose(_remove_tags, TakeFirst()),
         'out': _find_dates} 
    CATEGORY_PROCESSORS['Pages'] =                              \
        {'in': _default_input_processor,
         'out': _default_output_processor} 
    CATEGORY_PROCESSORS['Links'] = CATEGORY_PROCESSORS['Pages']

#%%
## definition of THEME paths and processors

try:
    assert THEME_PATHS
    assert not (THEME_PATHS in (None,{}) or all([v in ([],'',None) for v in THEME_PATHS.values()]))
except (NameError,AssertionError):
    THEME_PATHS      = {}
    ## Title
    #    <title>Living conditions - Statistics Explained</title>
    #    <h1 id="firstHeading" class="firstHeading"> Living conditions		</h1>
    THEME_PATHS['Title'] =                                      \
        xpath.create(first='h1[@id="firstHeading"]', 
                     tag='text()[normalize-space(.)]')
    # that is:
    #   '//h1[@id="firstHeading"]/text()[normalize-space(.)]'    
    ## Language
    THEME_PATHS['Language'] =                                   \
        xpath.create(node='html',                            
                     tag='@lang')
    # nothing else than: '//html/@lang'
    ## Last_modified
    #THEME_PATHS['Last_modified'] =                             \
    ## Statistical_articles
    THEME_PATHS['Statistical_articles'] =                       \
        xpath.create(first='h2',
                     tag='a/@href',
                     identifier='span[@id="Statistical_articles"]',
                     following_sibling=True,
                     preceding_sibling='*[starts-with(name(),"h")][1]',
                     sep='//')
    # that is:
    #   '//h2[span[@id="Statistical_articles"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Statistical_articles"]]]//a/@href'
    ## Topics (subset of Statistical_articles)
    THEME_PATHS['Topics'] =                                     \
        xpath.create(first='h4',
                     tag='a/@href',
                     identifier='span[@id="Topics"]',
                     following_sibling=True,
                     preceding_sibling='*[starts-with(name(),"h")][1]',
                     sep='//')
    # that is:
    #   '//h2[span[@id="Statistical_articles"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Statistical_articles"]]]//a/@href'
    ## Online_publications
    THEME_PATHS['Online_publications'] =                        \
        xpath.create(first='h2',
                     tag='a/@href',
                     identifier='span[@id="Online_publications"]',
                     following_sibling=True,
                     preceding_sibling='*[starts-with(name(),"h")][1]',
                     sep='//')
    # that is:
    #   '//h2[span[@id="Online_publications"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Online_publications"]]]//a/@href'
    ## Overview
    THEME_PATHS['Overview'] =                                   \
        xpath.create(first='h4',
                     tag='a/@href',
                     identifier='span[@id="Overview"]',
                     following_sibling=True,
                     preceding_sibling='*[starts-with(name(),"h")][1]',
                     sep='//')
    # that is:
    #   '//h4[span[@id="Overview"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Overview"]]]//a/@href'
    ## Background_articles
    THEME_PATHS['Background_articles'] =                        \
        xpath.create(first='h4',
                     tag='a/@href',
                     identifier='span[@id="Background_articles"]',
                     following_sibling=True,
                     preceding_sibling='*[starts-with(name(),"h")][1]',
                     sep='//')
    # that is:
    #   '//h4[span[@id="Background_articles"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Background_articles"]]]//a/@href'   
    ## Glossary
    THEME_PATHS['Glossary'] =                                   \
        xpath.create(first='h4',
                     tag='a/@href',
                     identifier='span[@id="Glossary"]',
                     following_sibling=True,
                     preceding_sibling='*[starts-with(name(),"h")][1]',
                     sep='//')
    # that is:
    #   '//h4[span[@id="Glossary"]]//following-sibling::*[preceding-sibling::*[starts-with(name(),"h")][1][span[@id="Glossary"]]]//a/@href'
    THEME_PATHS['Links'] = THEME_PATHS['Statistical_articles'] 
    # + THEME_PATHS['Background_articles'] + THEME_PATHS['Glossary']

try:
    assert THEME_PROCESSORS
    assert not (THEME_PROCESSORS in (None,{}) or all([v in ([],'',None) for v in THEME_PROCESSORS.values()]))
except (NameError,AssertionError):
    THEME_PROCESSORS = {}
    THEME_PROCESSORS['Title'] =                                 \
        {'in':  TakeFirst(),
         'out': _default_output_processor} 
    THEME_PROCESSORS['Language'] =                              \
        {'in':  TakeFirst(),
         'out': _default_output_processor} 
     #THEME_PROCESSORS['Last_modified'] =                        \
    #    {'in':  Compose(_remove_tags, TakeFirst()),
    #     'out': _find_dates} 
    THEME_PROCESSORS['Statistical_articles'] =                  \
        {'in': _default_input_processor,
         'out': _default_output_processor} 
    THEME_PROCESSORS['Topics'] =                                \
        {'in': _default_input_processor,
         'out': _default_output_processor} 
    THEME_PROCESSORS['Online_publications'] =                   \
        {'in': _default_input_processor,
         'out': _default_output_processor} 
    THEME_PROCESSORS['Overview'] =                              \
        {'in': _default_input_processor,
         'out': _default_output_processor} 
    THEME_PROCESSORS['Background_articles'] =                   \
        {'in': _default_input_processor,
         'out': _default_output_processor} 
    THEME_PROCESSORS['Glossary'] =                              \
        {'in': _default_input_processor,
         'out': _default_output_processor} 
    THEME_PROCESSORS['Links'] = THEME_PROCESSORS['Statistical_articles'] 

#%%
## definition of CONCEPT paths and processors

try:
    assert CONCEPT_PATHS
    assert not (CONCEPT_PATHS in (None,{}) or all([v in ([],'',None) for v in CONCEPT_PATHS.values()]))
except (NameError,AssertionError):
    CONCEPT_PATHS = GLOSSARY_PATHS

try:
    assert CONCEPT_PROCESSORS
    assert not (CONCEPT_PROCESSORS in (None,{}) or all([v in ([],'',None) for v in CONCEPT_PROCESSORS.values()]))
except (NameError,AssertionError):
    CONCEPT_PROCESSORS = GLOSSARY_PROCESSORS

#%%
SE_PAGES_PATHS      = {settings.GLOSSARY_KEY:   GLOSSARY_PATHS,
                       settings.CATEGORY_KEY:   CATEGORY_PATHS,
                       settings.ARTICLE_KEY:    ARTICLE_PATHS,
                       settings.THEME_KEY:      THEME_PATHS,
                       settings.CONCEPT_KEY:    CONCEPT_PATHS}

SE_PAGES_PROCESSORS = {settings.GLOSSARY_KEY:   GLOSSARY_PROCESSORS,
                       settings.CATEGORY_KEY:   CATEGORY_PROCESSORS,
                       settings.ARTICLE_KEY:    ARTICLE_PROCESSORS,
                       settings.THEME_KEY:      THEME_PROCESSORS,
                       settings.CONCEPT_KEY:    CONCEPT_PROCESSORS}

#%%
#==============================================================================
# START PAGES
#==============================================================================

## definition of specific pages paths and processors

try:
    assert WHATLINKS_PATHS
    assert not (WHATLINKS_PATHS in (None,{}) or all([v in ([],'',None) for v in WHATLINKS_PATHS.values()]))
except (NameError,AssertionError):
    WHATLINKS_PATHS = {}
    ## Links
    WHATLINKS_PATHS['Links'] =                                  \
        xpath.create(first='ul[@id="mw-whatlinkshere-list"]',
                     tag='li/a[1]/@href',
                     # tag='li/a[not(@title="Special:WhatLinksHere")]/@href',
                     child=True,
                     sep='//')
        # '//ul[@id="mw-whatlinkshere-list"]//li/a[1]/@href'
    ## Language
    WHATLINKS_PATHS['Language'] =                               \
        xpath.create(node='html',                            
                     tag='@lang')
    # nothing else than: '//html/@lang'
    
    
# CATEGORIES_PAGE: xpaths for specific scraping of the "Statistical themes" webpage, e.g. 
# http://ec.europa.eu/eurostat/statistics-explained/index.php?title=Special:Categories&offset=&limit=1000
try:
    assert CATEGORIES_PAGE_PATHS
    assert not (CATEGORIES_PAGE_PATHS in (None,{}) or all([v in ([],'',None) for v in CATEGORIES_PAGE_PATHS.values()]))
except (NameError,AssertionError):
    CATEGORIES_PAGE_PATHS = {}
    CATEGORIES_PAGE_PATHS['Links'] =                            \
        xpath.create(last='div[@class="printfooter"]',
                     tag='ul[1]/li/a/@href',
                     preceding=True)
    # that is:
    #   '//div[@class="printfooter"]/preceding::ul[1]/li/a/@href'


# THEMES_PAGE: xpaths for specific scraping of the "Statistical themes" webpage, e.g. 
# http://ec.europa.eu/eurostat/statistics-explained/index.php/Statistical_themes
try:
    assert THEMES_PAGE_PATHS
    assert not (THEMES_PAGE_PATHS in (None,{}) or all([v in ([],'',None) for v in THEMES_PAGE_PATHS.values()]))
except (NameError,AssertionError):
    THEMES_PAGE_PATHS = {}
    THEMES_PAGE_PATHS['Themes'] =                               \
        xpath.create(first='h3[@class="panel-title"]',
                     tag='a/@href',
                     descendant=True)
    # that is:
    #   '//h3[@class="panel-title"]//descendant::a/@href'
    THEMES_PAGE_PATHS['Links'] =                                \
        xpath.create(node='h1[@id="firstHeading"]', # h1[normalize-space(text())="Statistical themes"]
                     tag='a/@href',
                     following='div[@class="panel-body"]',
                     sep='//')
    # that is:
    #   '//h1[@id="firstHeading"]//following::div[@class="panel-body"]//a/@href'

# ARTICLES_PAGE: xpaths for specific scraping of the "All articles" webpage, e.g. 
# http://ec.europa.eu/eurostat/statistics-explained/index.php/All_articles
try:
    assert ARTICLES_PAGE_PATHS
    assert not (ARTICLES_PAGE_PATHS in (None,{}) or all([v in ([],'',None) for v in ARTICLES_PAGE_PATHS.values()]))
except (NameError,AssertionError):
    ARTICLES_PAGE_PATHS = {}
    # check: the paths are exactly as those used for STATISTICAL_THEMES_PATHS
    ARTICLES_PAGE_PATHS['Themes'] =                             \
        xpath.create(first='h3[@class="panel-title"]',
                     tag='a/@href',
                     descendant=True)
    # that is:
    #   '//h3[@class="panel-title"]//descendant::a/@href'
    ARTICLES_PAGE_PATHS['Links'] =                              \
        xpath.create(node='h1[@id="firstHeading"]', # h1[normalize-space(text())="Statistical themes and subthemes"]
                     tag='a/@href',
                     following='div[@class="panel-body"]',
                     sep='//')
    # that is:
    #   '//h1[@id="firstHeading"]//following::div[@class="panel-body"]//a/@href'

# GLOSSARIES_PAGE: xpaths for specific scraping of the "Thematic glossaries" webpage, 
# e.g. http://ec.europa.eu/eurostat/statistics-explained/index.php/Thematic_glossaries
try:
    assert GLOSSARIES_PAGE_PATHS
    assert not (GLOSSARIES_PAGE_PATHS in (None,{}) or all([v in ([],'',None) for v in GLOSSARIES_PAGE_PATHS.values()]))
except (NameError,AssertionError):
    GLOSSARIES_PAGE_PATHS = {}
    GLOSSARIES_PAGE_PATHS['Themes'] =                           \
        xpath.create(first='h3[@class="panel-title"]',
                     tag='a/@href',
                     descendant=True)
    # that is:
    #   '//h3[@class="panel-title"]//descendant::a/@href'
    GLOSSARIES_PAGE_PATHS['Links'] =                            \
        xpath.create(node='h1[@id="firstHeading"]', # h1[normalize-space(text())="Statistical themes and subthemes"]
                     tag='a/@href',
                     following='div[@class="panel-body"]',
                     sep='//')
    # that is:
    #   '//h1[@id="firstHeading"]//following::div[@class="panel-body"]//a/@href'
    GLOSSARIES_PAGE_PATHS['Special_topic'] =                     \
        xpath.create(node='h2[span[@id="Special-topic_glossaries"]]',
                     tag='a/@href',
                     following='table/tr/td',
                     sep='//')
    # that is:
    #   '//h2[span[@id="Special-topic_glossaries"]]//following::table/tr/td//a/@href'

# CONCEPTS_PAGE: xpaths for specific scraping of the "Statistical concept" webpage, 
# e.g. http://ec.europa.eu/eurostat/statistics-explained/index.php/Category:Statistical_concept
try:
    assert CONCEPTS_PAGE_PATHS
    assert not (CONCEPTS_PAGE_PATHS in (None,{}) or all([v in ([],'',None) for v in CONCEPTS_PAGE_PATHS.values()]))
except (NameError,AssertionError):
    CONCEPTS_PAGE_PATHS = {}
    CONCEPTS_PAGE_PATHS['Links'] =                              \
        xpath.create(node='h2[contains(normalize-space(text()),"Statistical concept")]',
                     tag='a/@href',
                     following='table/tr/td',
                     sep='//')
    # that is:
    #   '//h2[contains(normalize-space(text()),"Statistical concept")]//following::table/tr/td//a/@href'

SE_START_PAGES_PATHS = {settings.GLOSSARY_KEY:  GLOSSARIES_PAGE_PATHS,
                       settings.CATEGORY_KEY:   CATEGORIES_PAGE_PATHS,
                       settings.ARTICLE_KEY:    ARTICLES_PAGE_PATHS,
                       settings.THEME_KEY:      THEMES_PAGE_PATHS,
                       settings.CONCEPT_KEY:    CONCEPTS_PAGE_PATHS}

#SE_START_PAGES_PROCESSORS = {settings.GLOSSARY_KEY: GLOSSARIES_PAGE_PROCESSORS,
#                       settings.CATEGORY_KEY:   ARTICLES_PAGE_PROCESSORS,
#                       settings.ARTICLE_KEY:    ARTICLES_PAGE_PROCESSORS,
#                       settings.THEME_KEY:      THEMES_PAGE_PROCESSORS,
#                       settings.CONCEPT_KEY:    CCONCEPTS_PAGE_PROCESSORS}

#%%
#==============================================================================
# ITEM CLASSES
#==============================================================================
   
def __base_item_class(class_name, paths, **kwargs):
    processors = kwargs.get('processors', {})
    fields = defaultdict(scrapy.Field) 
    for key in paths.keys():
        try:
            fields[key] = scrapy.Field(
                            input_processor=processors[key]['in'],
                            output_processor=processors[key]['out']
                            )
        except KeyError:    # when either (i) PROCESSORS in ({},None), 
                            # or (ii) KEY is not a key in PROCESSORS 
            fields[key] = scrapy.Field()  
    return type(str(class_name), (scrapy.Item,), 
                {'fields': fields, 'paths': paths, 'processors': processors}
                )

GlossaryItem = __base_item_class('GlossaryItem', GLOSSARY_PATHS, 
                                 processors=GLOSSARY_PROCESSORS)

ArticleItem = __base_item_class('GlossaryItem', ARTICLE_PATHS, 
                                 processors=ARTICLE_PROCESSORS)

CategoryItem = __base_item_class('GlossaryItem', CATEGORY_PATHS, 
                                 processors=CATEGORY_PROCESSORS)

ThemeItem = __base_item_class('ThemeItem', THEME_PATHS, 
                                 processors=THEME_PROCESSORS)

ConceptItem = __base_item_class('ContextItem', CONCEPT_PATHS, 
                                 processors=CONCEPT_PROCESSORS)

WhatLinksItem = __base_item_class('WhatLinksItem', WHATLINKS_PATHS)
            
#from scrapy.item import BaseItem
#class _FlexibleItem(dict, BaseItem):
#   pass
#
#class __BaseItem(scrapy.Item):
#    processors, paths = {}, {}
#    _allowed_keys = []   
#    def __setitem__(self, key, value):
#        if key not in self._allowed_keys:
#            raise scrapyroError("Key %s not supported for glossary item" % key)
#        if key not in self.fields:
#            self.fields[key] = scrapy.Field(
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
#class ThemeItem(__BaseItem):
#    _allowed_keys = THEME_FIELDS
#    processors = THEME_PROCESSORS
#    paths = THEME_PATHS

SE_ITEMS            = {settings.GLOSSARY_KEY:   GlossaryItem,
                       settings.CATEGORY_KEY:   CategoryItem,
                       settings.ARTICLE_KEY:    ArticleItem,
                       settings.THEME_KEY:      ThemeItem,
                       settings.CONCEPT_KEY:    ConceptItem}

#%%
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
    
class ThemeItemLoader(__BaseItemLoader):
    def __init__(self, *args, **kwargs):
        return super(ThemeItemLoader,self).__init__(ThemeItem(), *args, **kwargs)
    
class ConceptItemLoader(__BaseItemLoader):
    def __init__(self, *args, **kwargs):
        return super(ConceptItemLoader,self).__init__(ConceptItem(), *args, **kwargs)

SE_ITEMLOADERS      = {settings.GLOSSARY_KEY:   GlossaryItemLoader,
                       settings.CATEGORY_KEY:   CategoryItemLoader,
                       settings.ARTICLE_KEY:    ArticleItemLoader,
                       settings.THEME_KEY:      ThemeItemLoader,
                       settings.CONCEPT_KEY:    ConceptItemLoader}
