#!/usr/bin/python3

# test_parse_multi_line.py
# Date:  12/04/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
from pprint import pprint

from lam4vb3.cell_parser import parse_multi_line_commented_value


def test_parse_multi_line_commented_value():
    multi_line_commented_value = """eurovoc:5541
eurovoc:889 | indicate also: country or region; type of business; aid to undertakings

    """
    results = parse_multi_line_commented_value(multi_line_commented_value, graph=None, language=None,
                                               data_type=None)
    assert len(results) == 2
    assert "889" in results[1][0]
    assert "country" in results[1][1]


def test_parse_multi_line_commented_value3():
    multi_line_commented_value = """
    eurovoc:1474 |country; subject

    """
    results = parse_multi_line_commented_value(multi_line_commented_value, graph=None, language=None,
                                               data_type=None)
    assert len(results) == 1
    assert results[0][1]


def test_parse_multi_line_commented_value2():
    multi_line_commented_value = """subject-matter:AIDE
subject-matter:AELE 
"""
    results = parse_multi_line_commented_value(multi_line_commented_value, graph=None, language=None,
                                               data_type=None)
    assert "AELE" in results[1][0]
