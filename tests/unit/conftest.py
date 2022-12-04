#!/usr/bin/python3

# conftest.py
# Date:  18/11/2020
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import json
import pathlib
import shutil

import pandas as pd
import pytest
import rdflib

import lam4vb3.lam_utils
from lam4vb3 import LAM_PROPERTIES_WS_NAME, LAM_CLASSES_WS_NAME, LAM_PROPERTY_CLASSIFICATION_WS_NAME, \
    LAM_CLASS_CLASSIFICATION_WS_NAME, CELEX_CLASSES_WS_NAME, CELEX_CLASS_CLASSIFICATION_WS_NAME, PREFIX_WS_NAME
from lam4vb3.builder.celex_classes_builder import make_celex_classes_worksheet
from lam4vb3.builder.lam_classes_builder import make_lam_classes_worksheet
from lam4vb3.builder.property_builder import make_property_worksheet
from lam4vb3.excel2rdf import transform_celex_classes, transform_properties, transform_classes
from lam4vb3.lam_utils import read_excel_worksheet
from tests import OUTPUT_FOLDER, THIS_PROJECT

SHACL_SHAPES_2021 = pathlib.Path(__file__).parent.parent.parent / "models" / "lam-skos-ap-2021.ttl"
# TESTBED_EXCEL_2021_08 = pathlib.Path(__file__).parent.parent / "test_data" / "LAM_metadata_20210413_testbed.xlsx"
TESTBED_EXCEL_2021_08 = pathlib.Path(
    __file__).parent.parent / "test_data" / "LAM_metadata_20210909-ECO-corr-2022-12-4.xlsx"
TEMP_OUTPUT_FOLDER = pathlib.Path(__file__).parent.parent / "output"
QUERIES_FOLDER = pathlib.Path(__file__).parent.parent / "queries"


# file fixtures

@pytest.fixture(scope="session")
def shacl_shapes() -> rdflib.Graph:
    result_graph = rdflib.Graph()
    result_graph.parse(source=str(SHACL_SHAPES_2021))
    return result_graph


# example queries

@pytest.fixture(scope="session")
def lam_property_author_query():
    path_to_query_file = QUERIES_FOLDER / "lam_property_author.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_property_author_example_query():
    path_to_query_file = QUERIES_FOLDER / "lam_property_author_example.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_property_date_effect_query():
    path_to_query_file = QUERIES_FOLDER / "lam_property_date_effect.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_property_legal_basis_query():
    path_to_query_file = QUERIES_FOLDER / "lam_property_legal_basis.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_property_addition_query():
    path_to_query_file = QUERIES_FOLDER / "lam_property_addition.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_property_classification_query():
    path_to_query_file = QUERIES_FOLDER / "lam_property_classification.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_classes_description_query():
    path_to_query_file = QUERIES_FOLDER / "lam_classes_description.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_classes_property_configuration_DD_query():
    path_to_query_file = QUERIES_FOLDER / "lam_classes_property_configuration_DD.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_classes_property_configuration_SG_query():
    path_to_query_file = QUERIES_FOLDER / "lam_classes_property_configuration_SG.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_classes_classify_with_query():
    path_to_query_file = QUERIES_FOLDER / "lam_classes_classify_with.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_class_classification_query():
    path_to_query_file = QUERIES_FOLDER / "lam_class_classification.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_celex_classes_query():
    path_to_query_file = QUERIES_FOLDER / "lam_celex_classes.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_celex_classes_classification_query():
    path_to_query_file = QUERIES_FOLDER / "lam_celex_classes_classification.rq"
    return path_to_query_file.read_text()


@pytest.fixture(scope="session")
def lam_celex_property_configuration_DTS_query():
    path_to_query_file = QUERIES_FOLDER / "lam_celex_property_configuration_DTS.rq"
    return path_to_query_file.read_text()


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
def test_lam_celex_classes_df():
    return read_excel_worksheet(file_path=TESTBED_EXCEL_2021_08, sheet_name=CELEX_CLASSES_WS_NAME)


@pytest.fixture(scope="session")
def test_lam_celex_classes_classification_df():
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
                         test_prefixes_df, ):
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    return make_property_worksheet(lam_df_properties=test_lam_properties_df,
                                   lam_df_property_classification=test_lam_properties_classification_df,
                                   prefixes=test_prefixes_df, output_file=OUTPUT_FOLDER / "lam_properties.ttl")


@pytest.fixture(scope="session")
def lam_classes_graph(test_lam_classes_df, test_lam_classes_classification_df,
                      test_prefixes_df, ):
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    return make_lam_classes_worksheet(lam_df_classes=test_lam_classes_df,
                                      lam_df_classes_classification=test_lam_classes_classification_df,
                                      prefixes=test_prefixes_df, output_file=OUTPUT_FOLDER / "lam_classes.ttl")


@pytest.fixture(scope="session")
def lam_celex_classes_graph(test_lam_celex_classes_df, test_lam_celex_classes_classification_df,
                            test_prefixes_df, ):
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    return make_celex_classes_worksheet(lam_df_celex_classes=test_lam_celex_classes_df,
                                        lam_df_celex_classes_classification=test_lam_celex_classes_classification_df,
                                        prefixes=test_prefixes_df, output_file=OUTPUT_FOLDER / "lam_celex_classes.ttl")
