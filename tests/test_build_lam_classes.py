"""
test_build_lam_classes.py
Date: 23/11/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""

import unittest

import pandas as pd
from rdflib.namespace import SKOS

from lam4vb3 import INPUT_EXCEL_FILE, PREFIX_WS_NAME, LAM_CLASSES_WS_NAME, class_build, \
    LAM_CLASSES_TTL


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.lam_df_classes = pd.read_excel(INPUT_EXCEL_FILE, sheet_name=LAM_CLASSES_WS_NAME, header=[0],
                                            na_values=[""],
                                            keep_default_na=False)
        self.prefixes = pd.read_excel(INPUT_EXCEL_FILE, sheet_name=PREFIX_WS_NAME,
                                      header=[0], na_values=[""], keep_default_na=False)

    def test_generating_classes(self):
        graph = class_build.make_class_worksheet(self.lam_df_classes, self.prefixes, LAM_CLASSES_TTL)

        assert (None, None, SKOS.Collection) in graph, "No collections defined"
        assert (None, None, SKOS.Concept) in graph, "No concepts defined"
        assert (None, None, SKOS.ConceptScheme) in graph, "No collections defined"


if __name__ == '__main__':
    unittest.main()
