#!/usr/bin/python3

# conftest.py
# Date:  18/11/2020
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import pytest


from lam4vb3.excel2rdf import transform_celex_classes, transform_properties, transform_classes


# @pytest.fixture(scope="session")
# def get_celex_classes_rdf():
#     return transform_celex_classes("test_data/LAM_metadata_20210413_testbed.xlsx", "test_data/rdf_output")
#
#
# @pytest.fixture(scope="session")
# def get_lam_proprieties_rdf():
#     return transform_properties("test_data/LAM_metadata_20210413_testbed.xlsx", "test_data/rdf_output")
#
#
# @pytest.fixture(scope="session")
# def get_lam_classes_rdf():
#     return transform_classes("test_data/LAM_metadata_20210413_testbed.xlsx", "test_data/rdf_output")
