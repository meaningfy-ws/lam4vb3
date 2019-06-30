"""
test_build
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import unittest
import pandas as pd
import numpy as np

from lam4vb3 import build


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.test_df = pd.DataFrame.from_dict(
            {'URI': {0: 'lamd:md_001', 1: 'lamd:md_002', 2: 'lamd:md_003', 3: 'lamd:md_004', 4: 'lamd:md_005'},
             'Code': {0: 'CODE', 1: 'LABEL', 2: 'KEYWORD', 3: 'EXAMPLE_EN', 4: 'EXAMPLE_FR'},
             'Label': {0: 'Concept code', 1: 'Label of the concept', 2: 'Keywords', 3: 'EN example', 4: 'FR example'},
             'property': {0: 'skos:notation', 1: 'skosxl:prefLabel@en', 2: 'skosxl:prefLabel@en', 3: 'skos:example@en',
                          4: 'skos:example@fr'},
             'controlled value _property': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'annotation_1': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'controlled value_annotation_1 ': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'annotation_2': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'controlled value_annotation_2': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'annotation_3': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'controlled value_annotation_3': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'annotation_4': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'controlled value_annotation_4': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'annotation_5': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'controlled value_annotation_5': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'annotation_6': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'controlled value_annotation_6': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'annotation_7': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'controlled value_annotation_7': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'Definition': {0: np.nan, 1: np.nan,
                            2: 'Field used in the cataloguing methodology for classification and search purposes. '
                               'Keywords are usually extracted from the titles of documents.',
                            3: 'Field used in the cataloguing methodology for  information purposes. ',
                            4: 'Field used in the cataloguing methodology for  information purposes. '},
             'Example - cellar notice': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'Analytical methodology': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'Specific cases': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'Comments': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'Changes to be done': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'Is this metadata concerned by the legal analysis?': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan,
                                                                   4: np.nan},
             'Classification level 1': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan},
             'Classification level 2': {0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan}})

        self.column_mappings = {
            'Code': 'skos:notation',
            'Label': 'skos:prefLabel@en',
            'property': 'sh:path',
            'controlled value _property': 'sh:class',
            'Definition': 'skos:definition@en',
            'Example - cellar notice': 'skos:example',
            'Analytical methodology': 'skos:scopeNote@en',
            'Specific cases': 'skos:historyNote@en',
            'Comments': 'skos:editorialNote@en',
            'Changes to be done': 'skos:editorialNote@en',
        }

        self.graph = build.make_lam_graph()

    def test_simple_triple_maker(self):
        s = build.SimpleTripleMaker(df=self.test_df, column_mapping_dict=self.column_mappings, graph=self.graph)
        triples = s.make_column_triples(target_column="Label", )
        print(len(triples))
        assert len(triples) > 4, "Must have some triples generated"
        assert len(self.graph) > 4, "Must have some triples in the graph"

    def test_reified_triple_maker(self):
        s = build.ReifiedTripleMaker(df=self.test_df, column_mapping_dict=self.column_mappings, graph=self.graph)
        triples = s.make_column_triples(target_column="Label", )
        assert len(triples) > 14, "Must have some triples generated"
        assert len(self.graph) > 14, "Must have some triples in the graph"


if __name__ == '__main__':
    unittest.main()
