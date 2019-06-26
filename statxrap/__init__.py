#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. _statxrap__init__.py

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
                        ('package', 'statxrap'),
                        ('date', 'Mon Dec 18 17:28:29 2017'),
                        ('url', 'https://github.com/gjacopo/statxweb'),
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

class SXrapError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, msg, expr=None):    
        self.msg = msg
        if expr is not None:    self.expr = expr
    def __str__(self):              return repr(self.msg)
class SXrapWarning(Warning):
    """Base class for warnings in this module."""
    def __init__(self, msg, expr=None):    
        self.msg = msg
        if expr is not None:    self.expr = expr
    def __str__(self):              return repr(self.msg)

