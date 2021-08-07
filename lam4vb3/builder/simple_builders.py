#!/usr/bin/python3

# simple_builders.py
# Date:  04/08/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
from abc import ABC
from typing import List, Tuple, Dict

import pandas as pd
import rdflib
from rdflib import SKOS

from lam4vb3.builder.base_builders import AbstractTripleMaker
from lam4vb3.cell_parser import LITERAL_VALUE, VALUES, COMMENT


class SimpleTripleMaker(AbstractTripleMaker):
    """
        Create triples using cell values as direct objects.

        The considered interpretations are: Literal values and
        lists of URI values (optionally comments are added to
        the concept if any available).
    """
    def __init__(self, df: pd.DataFrame,
                 column_mapping_dict: Dict,
                 graph: rdflib.Graph,
                 comment_predicate: SKOS.editorialNote,
                 target_columns: List[str] = [],
                 literal_columns: List[str] = [],
                 subject_source_column: str = "URI",
                 subject_classes: List[rdflib.URIRef] = [SKOS.Concept],
                 ):
        """
        :type subject_in_scheme: the concept scheme in which all the rows will be placed
        """
        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         target_columns=target_columns,
                         subject_source_column=subject_source_column,
                         literal_columns=literal_columns,
                         subject_classes=subject_classes)
        self.comment_predicate = comment_predicate

    def make_cell_triples(self, row_index, target_column: str) -> List[Tuple]:
        cell_interpretation = self.handle_cell_value(row_index=row_index, target_column=target_column)

        row_subject = self.handle_row_uri(row_index=row_index)
        column_predicate = self.handle_column_predicate(target_column=target_column)

        if LITERAL_VALUE in cell_interpretation:
            predicate_language = self.handle_literal_language_from_predicate_signature(target_column=target_column)
            return [(row_subject, column_predicate,
                     rdflib.Literal(cell_interpretation[LITERAL_VALUE], lang=predicate_language))]
        elif VALUES in cell_interpretation:
            result = [(row_subject, column_predicate, value) for value in cell_interpretation[VALUES]]
            if COMMENT in cell_interpretation:
                result.append((row_subject, self.comment_predicate, rdflib.Literal(cell_interpretation[COMMENT])))
            return result

        return []


class ConceptTripleMaker(SimpleTripleMaker):
    """
       A base class for creating concepts.
       Creates inScheme statements from cell values attached to a concept using the following pattern.

    """

    def __init__(self, df: pd.DataFrame,
                 column_mapping_dict: Dict,
                 graph: rdflib.Graph,
                 subject_in_scheme: rdflib.URIRef,
                 comment_predicate: SKOS.editorialNote,
                 target_columns: List[str] = [],
                 literal_columns: List[str] = [],
                 subject_source_column: str = "URI",
                 subject_classes: List[rdflib.URIRef] = [SKOS.Concept],
                 ):
        """
        :type subject_in_scheme: the concept scheme in which all the rows will be placed
        """
        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         target_columns=target_columns,
                         subject_source_column=subject_source_column,
                         literal_columns=literal_columns,
                         subject_classes=subject_classes,
                         comment_predicate=comment_predicate)
        self.subject_in_scheme = subject_in_scheme

    def make_row_triples(self, row_index) -> List[Tuple]:
        result_triples = super().make_row_triples(row_index=row_index)
        if self.subject_in_scheme:
            row_subject = self.handle_row_uri(row_index=row_index, )
            result_triples.append((row_subject, SKOS.inScheme, self.subject_in_scheme))
        return result_triples

