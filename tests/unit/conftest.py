#!/usr/bin/python3

# conftest.py
# Date:  18/11/2020
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import json
import pathlib
import pytest
import rdflib

from lam4vb3.excel2rdf import transform_celex_classes, transform_properties, transform_classes

SHACL_SHAPES_2021 = pathlib.Path(__file__).parent.parent.parent / "models" / "lam-skos-ap-2021.ttl"

@pytest.fixture(scope="session")
def get_celex_classes_rdf():
    return transform_celex_classes("../test_data/LAM_metadata_20210413_testbed.xlsx", "../test_data/rdf_output")


@pytest.fixture(scope="session")
def get_lam_proprieties_rdf():
    return transform_properties("../test_data/LAM_metadata_20210413_testbed.xlsx", "../test_data/rdf_output")


@pytest.fixture(scope="session")
def get_lam_classes_rdf():
    return transform_classes("../test_data/LAM_metadata_20210413_testbed.xlsx", "../test_data/rdf_output")

@pytest.fixture(scope="session")
def shacl_shapes() -> rdflib.Graph:

    result_graph = rdflib.Graph()
    result_graph.parse(source=str(SHACL_SHAPES_2021))
    return result_graph

