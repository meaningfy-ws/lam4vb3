import rdflib


def test_transform_lam_proprieties(get_lam_proprieties_rdf, lam_property_author_query, lam_property_author_example_query):
    result = get_lam_proprieties_rdf.query(lam_property_author_query)
    for row in result:
        assert row

    result = get_lam_proprieties_rdf.query(lam_property_author_example_query)
    for row in result:
        assert row
