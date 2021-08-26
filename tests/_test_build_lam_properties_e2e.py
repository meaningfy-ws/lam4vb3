"""
test_build_lam_properties.py
Date: 23/11/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""

import unittest

import pandas as pd
from rdflib.namespace import SKOS

from lam4vb3 import LAM_PROPERTIES_WS_NAME, PREFIX_WS_NAME, LAM_PROPERTY_CLASSIFICATION_WS_NAME
from lam4vb3.unused import property_build
from tests import INPUT_EXCEL_FILE, LAM_PROPERTIES_TTL


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.lam_df_properties = pd.read_excel(INPUT_EXCEL_FILE, sheet_name=LAM_PROPERTIES_WS_NAME,
                                               header=[0], na_values=[""], keep_default_na=False)
        self.lam_df_property_classification = pd.read_excel(INPUT_EXCEL_FILE,
                                                            sheet_name=LAM_PROPERTY_CLASSIFICATION_WS_NAME,
                                                            header=[0], na_values=[""], keep_default_na=False)
        self.prefixes = pd.read_excel(INPUT_EXCEL_FILE, sheet_name=PREFIX_WS_NAME,
                                      header=[0], na_values=[""], keep_default_na=False)

    def test_generating_properties(self):
        graph = property_build.make_property_worksheet(self.lam_df_properties, self.lam_df_property_classification,
                                                       self.prefixes, LAM_PROPERTIES_TTL)
        assert (None, None, SKOS.Collection) in graph, "No collections defined"
        assert (None, None, SKOS.Concept) in graph, "No concepts defined"
        assert (None, None, SKOS.ConceptScheme) in graph, "No collections defined"


if __name__ == '__main__':
    unittest.main()
