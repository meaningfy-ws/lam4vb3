import pathlib
from pyshacl import validate


def test_lam_classes(lam_classes_graph, shacl_shapes):
    r = validate(lam_classes_graph,
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


def test_lam_properties(lam_properties_graph, shacl_shapes):
    r = validate(lam_properties_graph,
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


def test_celex_classes(lam_celex_classes_graph, shacl_shapes):
    r = validate(lam_celex_classes_graph,
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
