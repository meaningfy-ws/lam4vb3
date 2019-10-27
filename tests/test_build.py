"""
test_build
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import unittest
import pandas as pd
import numpy as np
import rdflib

from lam4vb3 import build


class MyTestCase(unittest.TestCase):
    # TODO: make it run with the current code, or build a new test suite

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

        self.uri_valued_columns = ['property', 'controlled value _property']

        self.graph = build.make_lam_graph()

        # self.cell_value_variants_properties = [None, np.nan, "", "literal", "literal_line \nnew_line_literal",
        #                                        "skos:prefLabel",
        #                                        "skos:prefLabel\nskos:altLabel",
        #                                        ]

        self.multi_line_literals = ["literal", "literal_line \nnew_line_literal",
                                    "skos:prefLabel",
                                    "skos:prefLabel\nskos:altLabel", ]

        self.multi_line_uris = ["skos:prefLabel",
                                "skos:prefLabel\nskos:altLabel\nskos:note", ]

        self.multi_line_parse_value_and_comment_cell_examples = ["value ~ with another comment", "value1 \n value2",
                                                                 "value1 \n value2 | comment",
                                                                 "skos:prefLabel \n skos:altLabel ~ comment", ]

    def test_triple_maker(self):
        s = build.PlainColumnTripleMaker(df=self.test_df, column_mapping_dict=self.column_mappings,
                                         uri_valued_columns=self.uri_valued_columns, graph=self.graph)
        assert s.handle_subject("skos:Concept") == rdflib.URIRef(
            "http://www.w3.org/2004/02/skos/core#Concept"), "A concept is a concept"
        assert s.handle_predicate("Code") == rdflib.URIRef(
            "http://www.w3.org/2004/02/skos/core#notation"), "The code is a notation"
        assert s.handle_literal_language_from_predicate_signature("Label") == "en", "English language expected"

    def test_triple_maker_object_handling(self):
        s = build.PlainColumnTripleMaker(df=self.test_df, column_mapping_dict=self.column_mappings,
                                         uri_valued_columns=self.uri_valued_columns, graph=self.graph)
        assert s.handle_object("value", "Label", language="en") == rdflib.Literal("value",
                                                                                  lang="en"), "'value'@en expected"
        assert s.handle_object(None, "Label", ) is None, "None expected"
        assert s.handle_object("skos:prefLabel", "property") == rdflib.URIRef(
            "http://www.w3.org/2004/02/skos/core#prefLabel"), "skos:prefLabel expected"

    def test_triple_maker_object_multi_line(self):
        maker = build.PlainColumnTripleMaker(df=self.test_df, column_mapping_dict=self.column_mappings,
                                             uri_valued_columns=self.uri_valued_columns,
                                             multi_line_columns=["Label"], graph=self.graph)
        assert len(
            maker.handle_object("value1\nvalue2\nvalue3", "Label", language="en")) == 3, "multiple values expected"
        s = rdflib.URIRef("http://www.w3.org/2004/02/skos/core#s")
        p = rdflib.URIRef("http://www.w3.org/2004/02/skos/core#p")

        oo = maker.handle_object("value1\nvalue2\nvalue3", "Label", language="en")
        t = maker.make_cell_triples(s, p, oo)
        print(t)

    def test_simple_triple_maker(self):
        s = build.PlainColumnTripleMaker(df=self.test_df, column_mapping_dict=self.column_mappings,
                                         uri_valued_columns=self.uri_valued_columns, graph=self.graph)
        triples = s.make_column_triples(target_column="Label", )
        print(len(triples))
        assert len(triples) > 4, "Must have some triples generated"
        assert len(self.graph) > 4, "Must have some triples in the graph"

    def test_reified_triple_maker(self):
        s = build.ReifiedColumnTripleMaker(df=self.test_df, column_mapping_dict=self.column_mappings,
                                           uri_valued_columns=self.uri_valued_columns, graph=self.graph)
        triples = s.make_column_triples(target_column="Label", )
        assert len(triples) > 14, "Must have some triples generated"
        assert len(self.graph) > 14, "Must have some triples in the graph"

    def test_multi_line_values(self):
        for l in self.multi_line_literals:
            assert isinstance(build.parse_multi_line_value(l, language="en")[0],
                              rdflib.Literal), "expecting literals"

    def test_multi_line_uris(self):
        for l in self.multi_line_uris:
            assert isinstance(build.parse_multi_line_value(l, graph=self.graph)[0],
                              rdflib.URIRef), "expecting URIS"

    def test_parse_value_and_comment_cell(self):
        for l in self.multi_line_parse_value_and_comment_cell_examples:
            assert len(build.parse_commented_value(l)) == 2, "expecting tuples"

        assert build.parse_commented_value(self.multi_line_parse_value_and_comment_cell_examples[1])[1] is None, \
            "expecting a tuple with second value missing"

        for l in self.multi_line_parse_value_and_comment_cell_examples:
            assert 1 <= len(build.parse_multi_line_commented_value(l)) <= 2, "expecting one or two tuples"


if __name__ == '__main__':
    unittest.main()
