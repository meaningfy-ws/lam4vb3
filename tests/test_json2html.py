"""
test_json2html.py
Date: 15/12/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""

import unittest

from click.testing import CliRunner

from lam2doc import json2html, LAM_CLASSES_JSON, LAM_PROPERTIES_JSON, CELEX_CLASSES_JSON


class MyTestCase(unittest.TestCase):

    def test_lam_class_transform(self):
        runner = CliRunner()
        result = runner.invoke(json2html.transform,
                               [str(LAM_CLASSES_JSON), "--template", "lam_classes"])

        assert result.exit_code == 0
        assert (LAM_CLASSES_JSON.parent / LAM_CLASSES_JSON.stem / "main.html").exists(), "the folder does not exist"

    def test_lam_property_transform(self):
        runner = CliRunner()
        result = runner.invoke(json2html.transform,
                               [str(LAM_PROPERTIES_JSON), "--template", "lam_properties"])

        assert result.exit_code == 0
        assert (
                LAM_PROPERTIES_JSON.parent / LAM_PROPERTIES_JSON.stem / "main.html").exists(), "the folder does not exist"

    def test_celex_class_transform(self):
        runner = CliRunner()
        result = runner.invoke(json2html.transform,
                               [str(CELEX_CLASSES_JSON), "--template", "celex_classes"])
        print(result.exc_info)
        assert result.exit_code == 0
        assert (
                CELEX_CLASSES_JSON.parent / CELEX_CLASSES_JSON.stem / "main.html").exists(), "the folder does not exist"


if __name__ == '__main__':
    unittest.main()
