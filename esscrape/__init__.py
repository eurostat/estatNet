#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. _esscrape__init__.py

Initialisation file.

**About**

*credits*:      `gjacopo <jacopo.grazzini@ec.europa.eu>`_ 

*version*:      0.1
--
*since*:        Mon Dec 18 17:28:29 2017

**Usage**

    >>> from esscrape import *

"""

__all__ = ['spiders']#analysis:ignore

#==============================================================================
# PROGRAM METADATA
#==============================================================================

METADATA            = dict([
                        ('project', 'esscrape'),
                        ('date', 'Mon Dec 18 17:28:29 2017'),
                        ('url', 'https://github.com/gjacopo/esscrape'),
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

class essError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, msg, expr=None):    
        self.msg = msg
        if expr is not None:    self.expr = expr
    def __str__(self):              return repr(self.msg)
class essWarning(Warning):
    """Base class for warnings in this module."""
    def __init__(self, msg, expr=None):    
        self.msg = msg
        if expr is not None:    self.expr = expr
    def __str__(self):              return repr(self.msg)

