"""
test_jinja_generator.py
Date: 27.10.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""
import json
import shutil
import unittest
from pprint import pprint

from lam2doc.document_generator import JinjaGenerator
from tests import LAM_HELLO_WORLD_HTML, LAM_PROPERTY_CONTENT_JSON, LAM_PROPERTIES_HTML, LAM_CLASSES_HTML, \
    LAM_CLASS_CONTENT_JSON


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        with LAM_PROPERTY_CONTENT_JSON.open("r") as property_file:
            self.properties_data = json.load(property_file)
        with LAM_CLASS_CONTENT_JSON.open("r") as property_file:
            self.classes_data = json.load(property_file)

    def test_hello_world(self):
        gen = JinjaGenerator(main_template_name="hello_world.html")
        assert gen.generate(), "No page generated"
        shutil.rmtree(str(LAM_HELLO_WORLD_HTML), ignore_errors=True)
        gen.serialise(LAM_HELLO_WORLD_HTML)
        assert LAM_HELLO_WORLD_HTML.exists(), " No file created"

    def test_lam_property_generation(self):
        gen = JinjaGenerator(main_template_name="lam_properties.html", data=self.properties_data)
        assert gen.generate(), "No page generated"
        shutil.rmtree(str(LAM_PROPERTIES_HTML), ignore_errors=True)
        gen.serialise(LAM_PROPERTIES_HTML)
        assert LAM_PROPERTIES_HTML.exists(), " No file created"

    def test_lam_class_generation(self):
        gen = JinjaGenerator(main_template_name="lam_classes.html", data=self.classes_data)
        assert gen.generate(), "No page generated"
        shutil.rmtree(str(LAM_CLASSES_HTML), ignore_errors=True)
        gen.serialise(LAM_CLASSES_HTML)
        assert LAM_CLASSES_HTML.exists(), " No file created"


if __name__ == '__main__':
    unittest.main()
