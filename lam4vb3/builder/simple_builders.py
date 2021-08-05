#!/usr/bin/python3

# simple_builders.py
# Date:  04/08/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
from typing import List, Tuple

from lam4vb3.builder.base_builders import ConceptTripleMaker
from lam4vb3.cell_parser import LITERAL_VALUE, VALUES, COMMENT


class SimpleConceptTripleMaker(ConceptTripleMaker):
    """
        Create triples using cell values as direct objects.

        The considered interpretations are: Literal values and
        lists of URI values (optionally comments are added to
        the concept if any available).
    """

    def make_column_triples(self, target_column: str) -> List[Tuple]:
        return []

    def make_cell_triples(self, row_index, target_column: str) -> List[Tuple]:
        cell_interpretation = self.handle_cell_value(row_index=row_index, target_column=target_column)

        row_subject = self.handle_row_uri(row_index=row_index)
        column_predicate = self.handle_column_predicate(target_column=target_column)

        if LITERAL_VALUE in cell_interpretation:
            return [(row_subject, column_predicate, cell_interpretation[LITERAL_VALUE])]
        elif VALUES in cell_interpretation:
            result = [(row_subject, column_predicate, value) for value in cell_interpretation[VALUES]]
            if COMMENT in cell_interpretation:
                result.append((row_subject, self.comment_predicate, cell_interpretation[COMMENT]))
            return result


