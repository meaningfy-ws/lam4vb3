import pathlib
from pyshacl import validate

from tests.unit.conftest import get_lam_classes_rdf, get_lam_proprieties_rdf, get_celex_classes_rdf, shacl_shapes


def test_lam_classes(get_lam_classes_rdf, shacl_shapes):
    r = validate(get_lam_classes_rdf,
                 shacl_graph=shacl_shapes,
                 inference='rdfs',
                 abort_on_first=False,
                 allow_warnings=False,
                 meta_shacl=False,
                 advanced=False,
                 js=False,
                 debug=False)

    conforms, results_graph, results_text = r

    assert conforms


def test_lam_proprieties(get_lam_proprieties_rdf, shacl_shapes):
    r = validate(get_lam_proprieties_rdf,
                 shacl_graph=shacl_shapes,
                 inference='rdfs',
                 abort_on_first=False,
                 allow_warnings=False,
                 meta_shacl=False,
                 advanced=False,
                 js=False,
                 debug=False)

    conforms, results_graph, results_text = r

    assert conforms


def test_celex_classes(get_celex_classes_rdf, shacl_shapes):
    r = validate(get_celex_classes_rdf,
                 shacl_graph=shacl_shapes,
                 inference='rdfs',
                 abort_on_first=False,
                 allow_warnings=False,
                 meta_shacl=False,
                 advanced=False,
                 js=False,
                 debug=False)

    conforms, results_graph, results_text = r

    assert conforms
