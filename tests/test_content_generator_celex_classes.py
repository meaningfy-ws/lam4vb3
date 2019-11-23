"""
test_content_generator_celex_classes.py
Date: 23/11/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""
import shutil
import unittest

from lam2doc import CELEX_CLASSES_JSON, CELEX_CLASSES_XML
from lam2doc.content_generator import LAMGremlinGenerator
from lam4vb3 import CELEX_CLASSES_TTL


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.gen = LAMGremlinGenerator(str(CELEX_CLASSES_TTL), generate_collections=False)

    def test_initialisation(self):
        assert len(self.gen.rdf_graph) > 100, "the triples are not loaded "
        assert self.gen.g, "the property graph not connected"

    def test_serialisation_json(self):
        shutil.rmtree(str(CELEX_CLASSES_JSON), ignore_errors=True)
        self.gen.to_json(str(CELEX_CLASSES_JSON))
        assert CELEX_CLASSES_JSON.exists(), "File not created"

    def test_serialisation_xml(self):
        shutil.rmtree(str(CELEX_CLASSES_XML), ignore_errors=True)
        self.gen.to_xml(str(CELEX_CLASSES_XML))
        assert CELEX_CLASSES_XML.exists(), "File not created"


if __name__ == '__main__':
    unittest.main()
