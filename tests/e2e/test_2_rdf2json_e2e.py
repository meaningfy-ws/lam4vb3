"""
test_rdf2json.py
Date: 15/12/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""

import unittest

from lam2doc import rdf2json

from tests import LAM_PROPERTIES_TTL, LAM_CLASSES_TTL, CELEX_CLASSES_TTL, THIS_PROJECT, LAM_PROPERTIES_JSON, \
    LAM_CLASSES_JSON, CELEX_CLASSES_JSON
from click.testing import CliRunner


class MyTestCase(unittest.TestCase):

    def test_props_transform(self):
        runner = CliRunner()
        result = runner.invoke(rdf2json.transform,
                               [str(LAM_PROPERTIES_TTL), str(THIS_PROJECT / "data"), "--format", "json",
                                "--generate-collections"])

        assert result.exit_code == 0
        assert LAM_PROPERTIES_JSON.exists()

    def test_class_transform(self):
        runner = CliRunner()
        result = runner.invoke(rdf2json.transform,
                               [str(LAM_CLASSES_TTL), str(THIS_PROJECT / "data"), "--format", "json",
                                "--generate-collections"])

        assert result.exit_code == 0
        assert LAM_CLASSES_JSON.exists()

    def test_celex_class_transform(self):
        runner = CliRunner()
        result = runner.invoke(rdf2json.transform,
                               [str(CELEX_CLASSES_TTL), str(THIS_PROJECT / "data"), "--format", "json",
                                "--generate-collections"])

        assert result.exit_code == 0
        assert CELEX_CLASSES_JSON.exists()


if __name__ == '__main__':
    unittest.main()
