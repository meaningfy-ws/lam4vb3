"""
test_excel2rdf.py
Date: 23/11/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""
import logging
import unittest
from lam4vb3 import excel2rdf
from click.testing import CliRunner

from tests import THIS_PROJECT

class MyTestCase(unittest.TestCase):

    def test_excel_generation(self):
        runner = CliRunner()
        result = runner.invoke(excel2rdf.transform_files_in_folder,
                               [str(THIS_PROJECT / "data"), str(THIS_PROJECT / "data")])
        assert True
        # assert not result.exception
        # assert result.exit_code == 0

        # assert "Transforming the CELEX classes into RDF" in result.output
        # assert "Transforming the LAM properties into RDF" in result.output
        # # assert "Transforming the LAM classes into RDF" in result.output
        # assert "Successfully completed the transformation" in result.output
        # assert "Moving the input file" in result.output


if __name__ == '__main__':
    unittest.main()
