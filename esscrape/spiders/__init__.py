#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. __init__.py



**About**

*credits*:      `gjacopo <jacopo.grazzini@ec.europa.eu>`_ 

*version*:      0.1
--
*since*:        Mon Dec 18 17:28:29 2017


**Description**

**Usage**

    >>> import esspider
    
"""


__all__ = ['settings', 'base']#analysis:ignore

#==============================================================================
# PROGRAM METADATA
#==============================================================================

metadata = dict([
                ('project', 'esspider'),
                ('date', 'Mon Dec 18 17:28:29 2017'),
                ('url', 'https://github.com/gjacopo/esspider'),
                ('organization', 'European Union'),
                ('license', 'European Union Public Licence (EUPL)'),
                ('version', '0.1'),
                ('description', 'Tools for data collections upload from Eurostat website'),
                ('credits',  ['gjacopo']),
                ('contact', 'jacopo.grazzini@ec.europa.eu'),
                ])

#==============================================================================
# GLOBAL CLASSES/METHODS/VARIABLES
#==============================================================================

class ESSpiderError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, msg, expr=None):    
        self.msg = msg
        if expr is not None:    self.expr = expr
    def __str__(self):              return repr(self.msg)
class ESSpiderWarning(Warning):
    """Base class for warnings in this module."""
    def __init__(self, msg, expr=None):    
        self.msg = msg
        if expr is not None:    self.expr = expr
    def __str__(self):              return repr(self.msg)
