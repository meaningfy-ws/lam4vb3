from pyshacl import validate

from tests import OUTPUT_FOLDER


def test_lam_classes(lam_classes_graph, shacl_shapes):
    r = validate(lam_classes_graph,
                 shacl_graph=shacl_shapes,
                 inference='rdfs',
                 abort_on_first=False,
                 allow_warnings=False,
                 meta_shacl=True,
                 debug=True,
                 advanced=False)

    conforms, results_graph, results_text = r
    results_graph.serialize(str(OUTPUT_FOLDER / 'shacl_report_lam_classes.ttl'), format='turtle', )
    assert conforms


def test_lam_properties(lam_properties_graph, shacl_shapes):
    r = validate(lam_properties_graph,
                 shacl_graph=shacl_shapes,
                 inference='rdfs',
                 abort_on_first=False,
                 allow_warnings=False,
                 meta_shacl=True,
                 debug=True,
                 advanced=False)

    conforms, results_graph, results_text = r

    assert conforms


def test_celex_classes(lam_celex_classes_graph, shacl_shapes):
    r = validate(lam_celex_classes_graph,
                 shacl_graph=shacl_shapes,
                 inference='rdfs',
                 abort_on_first=False,
                 allow_warnings=False,
                 meta_shacl=True,
                 debug=True,
                 advanced=False)

    conforms, results_graph, results_text = r

    assert conforms
