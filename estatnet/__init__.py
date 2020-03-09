#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. _estatnet__init__.py

Initialisation file.

**About**

**Usage**

"""

# *credits*:      `gjacopo <jacopo.grazzini@ec.europa.eu>`_ 
# *since*:        Mon Dec 18 17:28:29 2017

__all__ = ['spiders']#analysis:ignore

#==============================================================================
# PROGRAM METADATA
#==============================================================================

METADATA            = dict([
                        ('package', 'EstatNet'),
                        ('date', 'Mon Dec 18 17:28:29 2017'),
                        ('url', 'https://github.com/gjacopo/EstatNet'),
                        ('organization', 'European Union'),
                        ('license', 'European Union Public Licence (EUPL)'),
                        ('version', '0.1'),
                        ('description', 'Tools for webscraping Eurostat website'),
                        ('credits',  ['gjacopo']),
                        ('contact', 'jacopo.grazzini@ec.europa.eu'),
                        ])

PACKAGES            = [
                        ]

#==============================================================================
# GENERIC WARNING/ERROR CLASSES
#==============================================================================

class ENetError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, msg, expr=None):    
        self.msg = msg
        if expr is not None:    self.expr = expr
    def __str__(self):              return repr(self.msg)
class ENetWarning(Warning):
    """Base class for warnings in this module."""
    def __init__(self, msg, expr=None):    
        self.msg = msg
        if expr is not None:    self.expr = expr
    def __str__(self):              return repr(self.msg)

#==============================================================================
# GENERIC XPATH BUILDER
#==============================================================================
    
class ENetXpath():
    """Class providing with the main (static) method (so-called 'xpath.create') 
    function used to "automatically" generate most of the rules that are needed
    to extract structured contents from webpage. 
    """

    @staticmethod
    def create(node=None, tag=None, first=None, last=None, identifier=None, 
               following_sibling=None, following=None, preceding_sibling=None, preceding=None, 
               ancestor=None, ancestor_self=None, descendant=None, descendant_self=None,
               parent=None, child=None, sep='/'):
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
        ancestor, ancestor_self : str               
            ancestor (or self) axes: True or expression of the relation (used with 
            "ancestor" and "ancestor-or-self" keywords respectively); default: None.
        child : str               
            child axe: True (simple '/' or '//' relation) or expression of the 
            relation; default: None.  
        following_sibling : str               
            following-sibling axe: True or expression of the relation (used with 
            "following-sibling" keyword); default: None.
        following : str               
            following axe: True or expression of the relation (used with "following" 
            keyword); default: None.
        descendant, descendant_self : str               
            descendant (or self) axes: True or expression of the relation (used with 
            "descendant" and "descendant-or-self" keywords respectively); default: None.
        sep:
            ; default: '/'.
            
        Returns
        -------
        path : str
            `xpath` formatted path to be used so as to extract a specific field 
            from a webpage.
        """
        ## default settings
        if last not in (None,'') and all([kw in (None,False,'') for kw in [preceding_sibling, preceding, ancestor, parent, ancestor_self]]):
            #warn(SXrapWarning("Parameter PRECEDING set to True with LAST"))
            preceding=True
        if first not in (None,'') and all([kw in (None,False,'') for kw in [following_sibling, following, child, descendant, descendant_self]]):
            #warn(SXrapWarning("Parameter CHILD set to True with FIRST"))
            child=True
        ## check
        if sum([kw not in ('', None) for kw in [preceding_sibling, preceding, ancestor, parent]]) > 1:
            raise ENetError("Incompatible keyword parameters (PRECEDING, PRECEDING_SIBLING, ANCESTOR, ANCESTOR_SELF, PARENT)")        
        elif sum([kw not in ('', None) for kw in [following_sibling, following, child, descendant]]) > 1:
            raise ENetError("Incompatible keyword parameters (FOLLOWING, FOLLOWING_SIBLING, DESCENDANT, DESCENDANT_SELF, CHILD)")        
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
        if not (last in (None,'') or all([kw in (None,True,'') for kw in [preceding_sibling, preceding, parent, ancestor, ancestor_self]])):
            raise ENetError("Instructions for (PRECEDING, PRECEDING_SIBLING, PARENT, ANCESTOR, ANCESTOR_SELF) incompatible with keyword parameter LAST")
        elif last in (None,'') and all([kw in (None,True,'') for kw in [preceding_sibling, preceding, parent, ancestor, ancestor_self]]):
            #SXrapWarning("Instructions for (PRECEDING, PRECEDING_SIBLING, ANCESTOR, PARENT) ignored in absence of parameter LAST")
            preceding_sibling = preceding = parent = ancestor = None
        if not (first in (None,'') or all([kw in (None,True,'') for kw in [following_sibling, following, child, descendant, descendant_self]])):
            raise ENetError("Instructions for (FOLLOWING, FOLLOWING_SIBLING, CHILD, DESCENDANT, DESCENDANT_SELF) incompatible with keyword parameter FIRST")
        elif first in (None,'') and all([kw in (None,True,'') for kw in [following_sibling, following, child, descendant, descendant_self]]):
            # this may ignored in case the default setting on first above is actually run
            #SXrapWarning("Parameters (FOLLOWING, FOLLOWING_SIBLING, DESCENDANT, CHILD) ignored in absence of parameter FIRST")
            following_sibling = following = child = descendant = None
        ## set
        prec, follow = '', ''
        if preceding_sibling not in ('', None):    prec, parent = 'preceding-sibling::', preceding_sibling
        elif preceding not in ('', None):          prec, parent = 'preceding::', preceding
        elif ancestor not in ('', None):           prec, parent = 'ancestor::', ancestor
        elif ancestor_self not in ('', None):      prec, parent = 'ancestor-or-self::', ancestor_self
        elif parent not in ('', None):             prec         = 'parent::' # parent unchanged
        else:                                      parent = None 
        if following_sibling not in ('', None):    follow, child = 'following-sibling::', following_sibling
        elif following not in ('', None):          follow, child = 'following::', following
        elif descendant not in ('', None):         follow, child = 'descendant::', descendant
        elif descendant_self not in ('', None):    follow, child = 'descendant-or-self::', descendant_self
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


