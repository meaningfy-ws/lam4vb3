"""
test_content_generator_classes.py
Date: 23/11/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""
import shutil
import unittest

from lam2doc import CONCEPT_QNAME, CONCEPT_SCHEME_QNAME, LAM_CLASSES_XML, LAM_CLASSES_JSON, COLLECTION_QNAME
from lam2doc.content_generator import LAMGremlinGenerator
from lam4vb3 import LAM_CLASSES_TTL


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.gen = LAMGremlinGenerator(str(LAM_CLASSES_TTL), generate_collections=True)

    def test_generation(self):
        content = self.gen.generate()
        assert CONCEPT_QNAME in content, "no concepts known"
        assert len(content[CONCEPT_QNAME]) > 0, "no concepts loaded"
        assert CONCEPT_SCHEME_QNAME in content, "no concept scheme known"
        assert len(content[CONCEPT_SCHEME_QNAME]) > 0, "no concept scheme loaded"
        assert COLLECTION_QNAME in content, "no collection known"
        assert len(content[COLLECTION_QNAME]) > 0, "no collection loaded"

    def test_serialisation_json(self):
        shutil.rmtree(str(LAM_CLASSES_JSON), ignore_errors=True)
        self.gen.to_json(str(LAM_CLASSES_JSON))
        assert LAM_CLASSES_JSON.exists(), "File not created"

    def test_serialisation_xml(self):
        shutil.rmtree(str(LAM_CLASSES_XML), ignore_errors=True)
        self.gen.to_xml(str(LAM_CLASSES_XML))
        assert LAM_CLASSES_XML.exists(), "File not created"


if __name__ == '__main__':
    unittest.main()
