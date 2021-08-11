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

# TODO: write such a test (passing test of course) for each SPARQL query.
