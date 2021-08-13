"""
test_build_celex_classes.py
Date: 23/11/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""

import unittest

import pandas as pd
from rdflib.namespace import SKOS

from lam4vb3 import PREFIX_WS_NAME, CELEX_CLASSES_WS_NAME, CELEX_CLASS_CLASSIFICATION_WS_NAME
from lam4vb3.unused import class_build
from tests import INPUT_EXCEL_FILE, CELEX_CLASSES_TTL


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.celex_df_classes = pd.read_excel(INPUT_EXCEL_FILE, sheet_name=CELEX_CLASSES_WS_NAME, header=[0],
                                              na_values=[""],
                                              dtype={"DTS": str, "CODE": str, },
                                              keep_default_na=False)

        self.celex_df_class_classification = pd.read_excel(INPUT_EXCEL_FILE,
                                                           sheet_name=CELEX_CLASS_CLASSIFICATION_WS_NAME,
                                                           dtype={"COMMENT": str, "DESCRIPTION": str, "ORDER": str,
                                                                  "PARENT": str},
                                                           header=[0], na_values=[""], keep_default_na=False)

        self.prefixes = pd.read_excel(INPUT_EXCEL_FILE, sheet_name=PREFIX_WS_NAME,
                                      header=[0], na_values=[""], keep_default_na=False)

    def test_generating_classes(self):
        graph = class_build.make_celex_class_worksheet(self.celex_df_classes, self.celex_df_class_classification,
                                                       self.prefixes, CELEX_CLASSES_TTL)
        assert (None, None, SKOS.Concept) in graph, "No concepts defined"
        assert (None, None, SKOS.ConceptScheme) in graph, "No collections defined"


if __name__ == '__main__':
    unittest.main()
