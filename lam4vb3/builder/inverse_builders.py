#!/usr/bin/python3

# inverse_builders.py
# Date:  04/08/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
from typing import Dict, List, Tuple

import pandas as pd
import rdflib

from lam4vb3 import cell_parser
from lam4vb3.builder.base_builders import AbstractTripleMaker
from lam4vb3.cell_parser import VALUES


class InverseTripleMaker(AbstractTripleMaker):
    """
        Builds triples from columns (which must contain URI references) to the row URI.
        The cells are assumed to be always URIs.
    """

    def __init__(self, df: pd.DataFrame,
                 column_mapping_dict: Dict,
                 graph: rdflib.Graph,
                 target_columns: List[str],
                 subject_source_column: str = "URI",
                 ):
        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         target_columns=target_columns,
                         subject_source_column=subject_source_column, )

    def make_cell_triples(self, row_index, target_column) -> List[Tuple]:
        row_subject = self.handle_row_uri(row_index=row_index)
        column_predicate = self.handle_column_predicate(target_column=target_column)

        cell_interpretation = cell_parser.parse_cell(cell_value=self.df.loc[row_index, target_column],
                                                     is_literal=False,
                                                     graph=self.graph)

        if VALUES in cell_interpretation:
            cell_values = cell_interpretation[VALUES]

            return [(value, column_predicate, row_subject)
                    for value in cell_values]
        return []