"""
test_excel2rdf.py
Date: 23/11/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""
import logging
import unittest
from lam4vb3 import excel2rdf, INPUT_EXCEL_FILE, THIS_PROJECT, LAM_PROPERTIES_TTL, CELEX_CLASSES_TTL, LAM_CLASSES_TTL
from click.testing import CliRunner


class MyTestCase(unittest.TestCase):

    def test_excel_generation(self):
        runner = CliRunner()
        result = runner.invoke(excel2rdf.transform, [str(INPUT_EXCEL_FILE), str(THIS_PROJECT / "data")])

        assert result.exit_code == 0
        assert LAM_PROPERTIES_TTL.exists()
        assert LAM_CLASSES_TTL.exists()
        assert CELEX_CLASSES_TTL.exists()


if __name__ == '__main__':
    unittest.main()
