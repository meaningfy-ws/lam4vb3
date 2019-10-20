"""
test_content_generator
Date: 20.10.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import unittest
from lam2doc.content_generator import *

LAM_PROPERTY_EXAMPLE = (
        pathlib.Path(__file__).resolve().parent.parent / "output/lam_project_properties_v2.ttl").resolve()

LAM_CLASS_EXAMPLE = (
        pathlib.Path(__file__).resolve().parent.parent / "output/lam_project_classes_v2.ttl").resolve()

LAM_PROPERTY_CONTENT_JSON = (
        pathlib.Path(__file__).resolve().parent.parent / "output/lam_project_properties.json").resolve()

LAM_CLASS_CONTENT_JSON = (
        pathlib.Path(__file__).resolve().parent.parent / "output/lam_project_classes.json").resolve()


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.gen = LAMGremlinGenerator(str(LAM_PROPERTY_EXAMPLE))

    def test_initialisation(self):
        assert len(self.gen.rdf_graph) > 100, "the triples are not loaded "
        assert self.gen.g, "the property graph not connected"

    def test_generation(self):
        content = self.gen.generate()
        assert CONCEPT_QNAME in content, "no concepts known"
        assert len(content[CONCEPT_QNAME]) > 0, "no concepts loaded"
        assert CONCEPT_SCHEME_QNAME in content, "no concept scheme known"
        assert len(content[CONCEPT_SCHEME_QNAME]) > 0, "no concept scheme loaded"

    def test_serialisation(self):
        self.gen.to_json(str(LAM_PROPERTY_CONTENT_JSON))


if __name__ == '__main__':
    unittest.main()
