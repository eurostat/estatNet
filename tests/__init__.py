#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. _tests__init__

Testing units.

*credits*:      `gjacopo <jacopo.grazzini@ec.europa.eu>`_ 

*version*:      0.1
--
*since*:        Sat Jan 27 20:00:50 2018


"""

#==============================================================================
# PROGRAM METADATA
#==============================================================================

from esscrape.metadata import metadata

metadata = metadata.copy()
metadata.update({ 
                'date': 'Sat Jan 27 20:00:50 2018',
                'credits':  ['grazzja']
                })


#==============================================================================
# CORE
#==============================================================================
 
__all__ = ['items']#analysis:ignore
