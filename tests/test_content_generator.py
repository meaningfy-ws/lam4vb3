"""
test_content_generator
Date: 20.10.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import shutil
import unittest

from lam2doc import CONCEPT_QNAME, CONCEPT_SCHEME_QNAME, COLLECTION_QNAME
from lam2doc.content_generator import LAMGremlinGenerator
from tests import LAM_PROPERTY_EXAMPLE, LAM_PROPERTY_CONTENT_JSON, LAM_PROPERTY_CONTENT_XML, LAM_CLASS_CONTENT_JSON, \
    LAM_CLASS_EXAMPLE


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
        assert COLLECTION_QNAME in content, "no collection known"
        assert len(content[COLLECTION_QNAME]) > 0, "no collection loaded"

    def test_serialisation_json(self):
        shutil.rmtree(str(LAM_PROPERTY_CONTENT_JSON), ignore_errors=True)
        self.gen.to_json(str(LAM_PROPERTY_CONTENT_JSON))
        assert LAM_PROPERTY_CONTENT_JSON.exists(), "File not created"

    def test_serialisation_json_2(self):
        class_gen = LAMGremlinGenerator(str(LAM_CLASS_EXAMPLE))
        shutil.rmtree(str(LAM_CLASS_CONTENT_JSON), ignore_errors=True)
        class_gen.to_json(str(LAM_CLASS_CONTENT_JSON))
        assert LAM_CLASS_CONTENT_JSON.exists(), "File not created"

    def test_serialisation_xml(self):
        shutil.rmtree(str(LAM_PROPERTY_CONTENT_XML), ignore_errors=True)
        self.gen.to_xml(str(LAM_PROPERTY_CONTENT_XML))
        assert LAM_PROPERTY_CONTENT_XML.exists(), "File not created"


if __name__ == '__main__':
    unittest.main()
