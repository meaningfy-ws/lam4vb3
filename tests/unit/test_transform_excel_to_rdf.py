import pytest
import rdflib

from lam4vb3.builder.property_builder import make_property_worksheet
from tests import OUTPUT_FOLDER


# def test_transform_lam_proprieties(get_lam_proprieties_rdf, lam_property_author_query,
#                                    lam_property_author_example_query):
#     result = get_lam_proprieties_rdf.query(lam_property_author_query)
#
#     assert len(result) > 0
#
#     result = get_lam_proprieties_rdf.query(lam_property_author_example_query)
#     for row in result:
#         assert row


def test_lam_property_author_query(lam_property_author_query, lam_properties_graph):
    results = lam_properties_graph.query(lam_property_author_query)
    assert results.askAnswer is True


def test_lam_property_author_example_query(lam_property_author_example_query, lam_properties_graph):
    results = lam_properties_graph.query(lam_property_author_example_query)
    assert results.askAnswer is True


def test_lam_properties_date_effect_query(lam_property_date_effect_query, lam_properties_graph):
    results = lam_properties_graph.query(lam_property_date_effect_query)
    assert results.askAnswer is True


def test_lam_property_legal_basis_query(lam_property_legal_basis_query, lam_properties_graph):
    results = lam_properties_graph.query(lam_property_legal_basis_query)
    assert results.askAnswer is True


def test_lam_property_addition_query(lam_property_addition_query, lam_properties_graph):
    results = lam_properties_graph.query(lam_property_addition_query)
    assert results.askAnswer is True


def test_lam_property_classification_query(lam_property_classification_query, lam_properties_graph):
    results = lam_properties_graph.query(lam_property_classification_query)
    assert results.askAnswer is True


def test_lam_classes_description_query(lam_classes_description_query, lam_classes_graph):
    results = lam_classes_graph.query(lam_classes_description_query)
    assert results.askAnswer is True


def test_lam_classes_property_configuration_DD_query(lam_classes_property_configuration_DD_query, lam_classes_graph):
    results = lam_classes_graph.query(lam_classes_property_configuration_DD_query)
    assert results.askAnswer is True
# TODO: implement hasAnnotationConfiguration (ticket exists!)

def test_lam_classes_property_configuration_MI_query(lam_classes_property_configuration_MI_query, lam_classes_graph):
    results = lam_classes_graph.query(lam_classes_property_configuration_MI_query)
    assert results.askAnswer is True
# TODO: use an Y instead of O

def test_lam_classes_classify_with_query(lam_classes_classify_with_query, lam_classes_graph):
    results = lam_classes_graph.query(lam_classes_classify_with_query)
    assert results.askAnswer is True


def test_lam_class_classification_query(lam_class_classification_query, lam_classes_graph):
    results = lam_classes_graph.query(lam_class_classification_query)
    assert results.askAnswer is True


def test_lam_celex_classes_query(lam_celex_classes_query, lam_celex_classes_graph):
    results = lam_celex_classes_graph.query(lam_celex_classes_query)
    assert results.askAnswer is True

def test_lam_celex_classes_classification_query(lam_celex_classes_classification_query, lam_celex_classes_graph):
    results = lam_celex_classes_graph.query(lam_celex_classes_classification_query)
    assert results.askAnswer is True