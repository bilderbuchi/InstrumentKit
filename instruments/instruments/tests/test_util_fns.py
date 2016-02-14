#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# test_util_fns.py: Tests various utility functions.
##
# © 2013-2015 Steven Casagrande (scasagrande@galvant.ca).
#
# This file is a part of the InstrumentKit project.
# Licensed under the AGPL version 3.
##
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
##

## IMPORTS ####################################################################

from __future__ import absolute_import
from builtins import range

import quantities as pq

from nose.tools import raises, eq_

from instruments.util_fns import (
    ProxyList,
    assume_units, convert_temperature
)

from enum import Enum

## TEST CASES #################################################################

def test_ProxyList_basics():
    class ProxyChild(object):
        def __init__(self, parent, name):
            self._parent = parent
            self._name = name
            
    parent = object()
    
    proxy_list = ProxyList(parent, ProxyChild, range(10))
    
    child = proxy_list[0]
    assert child._parent is parent
    assert child._name == 0
    
def test_ProxyList_valid_range_is_enum():
    class ProxyChild(object):
        def __init__(self, parent, name):
            self._parent = parent
            self._name = name
            
    class MockEnum(Enum):
        a = "aa"
        b = "bb"
        
    parent = object()
    
    proxy_list = ProxyList(parent, ProxyChild, MockEnum)
    assert proxy_list['aa']._name == MockEnum.a.value
    assert proxy_list['b']._name  == MockEnum.b.value
    assert proxy_list[MockEnum.a]._name == MockEnum.a.value
    
def test_ProxyList_length():
    class ProxyChild(object):
        def __init__(self, parent, name):
            self._parent = parent
            self._name = name
            
    parent = object()
    
    proxy_list = ProxyList(parent, ProxyChild, range(10))
    
    eq_(len(proxy_list), 10)
    
def test_ProxyList_iterator():
    class ProxyChild(object):
        def __init__(self, parent, name):
            self._parent = parent
            self._name = name
            
    parent = object()
    
    proxy_list = ProxyList(parent, ProxyChild, range(10))
    
    i = 0
    for item in proxy_list:
        eq_(item._name, i)
        i = i + 1

@raises(IndexError)
def test_ProxyList_invalid_idx_enum():
    class ProxyChild(object):
        def __init__(self, parent, name):
            self._parent = parent
            self._name = name
            
    class MockEnum(Enum):
        a = "aa"
        b = "bb"
        
    parent = object()
    
    proxy_list = ProxyList(parent, ProxyChild, MockEnum)
    
    proxy_list['c'] # Should raise IndexError
    
@raises(IndexError)
def test_ProxyList_invalid_idx():
    class ProxyChild(object):
        def __init__(self, parent, name):
            self._parent = parent
            self._name = name
        
    parent = object()
    
    proxy_list = ProxyList(parent, ProxyChild, range(5))
    
    proxy_list[10] # Should raise IndexError

def test_assume_units_correct():
    m = pq.Quantity(1, 'm')
    
    # Check that unitful quantities are kept unitful.
    eq_(assume_units(m, 'mm').rescale('mm').magnitude, 1000)
    
    # Check that raw scalars are made unitful.
    eq_(assume_units(1, 'm').rescale('mm').magnitude, 1000)

def test_temperature_conversion():
    blo = 70.0*pq.degF
    out = convert_temperature(blo, pq.degC)
    eq_(out.magnitude, 21.11111111111111)
    out = convert_temperature(blo, pq.degK)
    eq_(out.magnitude, 294.2055555555555)
    out = convert_temperature(blo, pq.degF)
    eq_(out.magnitude, 70.0)

    blo = 20.0*pq.degC
    out = convert_temperature(blo, pq.degF)
    eq_(out.magnitude, 68)
    out = convert_temperature(blo, pq.degC)
    eq_(out.magnitude, 20.0)
    out = convert_temperature(blo, pq.degK)
    eq_(out.magnitude, 293.15)

    blo = 270*pq.degK
    out = convert_temperature(blo, pq.degC)
    eq_(out.magnitude, -3.1499999999999773)
    out = convert_temperature(blo, pq.degF)
    eq_(out.magnitude, 141.94736842105263)
    out = convert_temperature(blo, pq.K)
    eq_(out.magnitude, 270)

@raises(ValueError)
def test_temperater_conversion_failure():
    blo = 70.0*pq.degF
    convert_temperature(blo, pq.V)

@raises(ValueError)
def test_assume_units_failures():
    assume_units(1, 'm').rescale('s')