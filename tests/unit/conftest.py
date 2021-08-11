#!/usr/bin/python3

# conftest.py
# Date:  18/11/2020
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import json
import pathlib

import pandas as pd
import pytest
import rdflib

import lam4vb3.lam_utils
from lam4vb3 import LAM_PROPERTIES_WS_NAME, LAM_CLASSES_WS_NAME, LAM_PROPERTY_CLASSIFICATION_WS_NAME, \
    LAM_CLASS_CLASSIFICATION_WS_NAME, CELEX_CLASSES_WS_NAME, CELEX_CLASS_CLASSIFICATION_WS_NAME, PREFIX_WS_NAME, \
    LAM_PROPERTIES_NEW_WS_NAME, build
from lam4vb3.builder.property_builder import make_property_worksheet
from lam4vb3.excel2rdf import transform_celex_classes, transform_properties, transform_classes
from lam4vb3.lam_utils import read_excel_worksheet
from tests import OUTPUT_FOLDER

SHACL_SHAPES_2021 = pathlib.Path(__file__).parent.parent.parent / "models" / "lam-skos-ap-2021.ttl"
TESTBED_EXCEL_2021_08 = pathlib.Path(__file__).parent.parent / "test_data" / "LAM_metadata_20210413_testbed.xlsx"
TEMP_OUTPUT_FOLDER = pathlib.Path(__file__).parent.parent / "output"


#  executions of the old transformers fixtures
#  TODO: to be refactored to file access
@pytest.fixture(scope="session")
def get_celex_classes_rdf():
    return transform_celex_classes(TESTBED_EXCEL_2021_08, TEMP_OUTPUT_FOLDER)


@pytest.fixture(scope="session")
def get_lam_proprieties_rdf():
    return transform_properties(TESTBED_EXCEL_2021_08, TEMP_OUTPUT_FOLDER)


@pytest.fixture(scope="session")
def get_lam_classes_rdf():
    return transform_classes(TESTBED_EXCEL_2021_08, TEMP_OUTPUT_FOLDER)


# file fixtures

@pytest.fixture(scope="session")
def shacl_shapes() -> rdflib.Graph:
    result_graph = rdflib.Graph()
    result_graph.parse(source=str(SHACL_SHAPES_2021))
    return result_graph


# example queries

@pytest.fixture(scope="session")
def lam_property_author_query():
    path_to_query_file = pathlib.Path(__file__).parent.parent / "queries" / "lam_property_author.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_property_author_example_query():
    path_to_query_file = pathlib.Path(__file__).parent.parent / "queries" / "lam_property_author_example.rq"
    return path_to_query_file.read_text()


# TODO: add fixtures for the rest opf the queries

# getting test data worksheets

@pytest.fixture(scope="session")
def test_lam_properties_df():
    return read_excel_worksheet(file_path=TESTBED_EXCEL_2021_08, sheet_name=LAM_PROPERTIES_WS_NAME)


@pytest.fixture(scope="session")
def test_lam_properties_classification_df():
    return read_excel_worksheet(file_path=TESTBED_EXCEL_2021_08, sheet_name=LAM_PROPERTY_CLASSIFICATION_WS_NAME)


@pytest.fixture(scope="session")
def test_lam_classes_df():
    return read_excel_worksheet(file_path=TESTBED_EXCEL_2021_08, sheet_name=LAM_CLASSES_WS_NAME)


@pytest.fixture(scope="session")
def test_lam_classes_classification_df():
    return read_excel_worksheet(file_path=TESTBED_EXCEL_2021_08, sheet_name=LAM_CLASS_CLASSIFICATION_WS_NAME)


@pytest.fixture(scope="session")
def test_celex_classes_df():
    return read_excel_worksheet(file_path=TESTBED_EXCEL_2021_08, sheet_name=CELEX_CLASSES_WS_NAME)


@pytest.fixture(scope="session")
def test_celex_classes_classification_df():
    return read_excel_worksheet(file_path=TESTBED_EXCEL_2021_08, sheet_name=CELEX_CLASS_CLASSIFICATION_WS_NAME)


@pytest.fixture(scope="session")
def test_prefixes_df():
    return read_excel_worksheet(file_path=TESTBED_EXCEL_2021_08, sheet_name=PREFIX_WS_NAME)


# default graph
@pytest.fixture(scope="function")
def empty_lam_graph(test_prefixes_df):
    return lam4vb3.lam_utils.make_graph(test_prefixes_df)


# result graphs fixtures

@pytest.fixture(scope="session")
def lam_properties_graph(test_lam_properties_df, test_lam_properties_classification_df,
                         test_prefixes_df,):
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    return make_property_worksheet(lam_df_properties=test_lam_properties_df,
                                   lam_df_property_classification=test_lam_properties_classification_df,
                                   prefixes=test_prefixes_df, output_file=OUTPUT_FOLDER / "lam_properties.ttl")


# TODO: add two more fixtures for lam classes and celex classes