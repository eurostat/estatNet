#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
..  _tests_base

Utility functions for esscrape unit test module 

**Dependencies**

*require*:      unittest, os, sys, re, warnings, time

**About**

**Description**

*credits*:      `gjacopo <jacopo.grazzini@ec.europa.eu>`_ 

*version*:      0.1
--
*since*:        Sat Jan 27 20:03:16 2018

**Contents**
"""


#==============================================================================
# PROGRAM METADATA
#==============================================================================

from kinki.__metadata__ import metadata as __metadata__
metadata = __metadata__.copy()
metadata.update({'date': 'Sat Jan 27 20:03:16 2018'})

#==============================================================================
# IMPORT STATEMENTS
#==============================================================================

import os, sys #analysis:ignore
import unittest
import re#analysis:ignore
import datetime, time#analysis:ignore


#==============================================================================
# GLOBAL VARIABLES/METHODS
#==============================================================================

assert metadata.project == 'esscrape' and metadata.package == 'esscrape'

#==============================================================================
# METHODS
#==============================================================================

#/****************************************************************************/
def __runonetest(testCase, **kwargs):
    try:
        t_class = testCase.__name__
        t_module = testCase.__module__
    except: raise IOError('unexpected input testing class entity')
    else:
        t_module_basename = t_module.split('.')[-1]        
    try:
        t_submodule = testCase.module
    except: raise IOError('unrecognised tested submodule')
    message = ''
    #message = '\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    message += '\n{}: Test {}.py module of {}.{}'
    print(message.format(t_class, t_submodule, metadata.package, t_module_basename))
    #warnings.warn()
    verbosity = kwargs.pop('verbosity',2)
    suite = unittest.TestLoader().loadTestsFromTestCase(testCase)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return

#/****************************************************************************/
def runtest(*TestCases, **kwargs):
    if len(TestCases)==0:                       
        return
    for testCase in TestCases:
        __runonetest(testCase, **kwargs)
        if len(TestCases)>1 and testCase!=TestCases[-1]: 
            time.sleep(1)
    return



