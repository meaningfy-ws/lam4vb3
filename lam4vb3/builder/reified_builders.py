#!/usr/bin/python3

# reified_builders.py
# Date:  05/08/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
from abc import ABC
from datetime import date
from typing import Dict, List, Tuple

import pandas as pd
import rdflib
from rdflib import RDF, XSD, DCTERMS

from lam4vb3 import lam_utils
from lam4vb3.builder.base_builders import AbstractTripleMaker
from lam4vb3.builder import SHACL
from lam4vb3.cell_parser import VALUES, MIN_COUNT, MAX_COUNT, COMMENT, NAME


class BaseConstraintTripleMaker(AbstractTripleMaker):
    """
        Creates triples for the property constraint columns.
        Lo literal columns are considered.
        The constraint definitions are reified objects.


        Creates constraint objects from cell values (once cell one constraint) attached to a concept using the following pattern

        row_subject a subject_class .
        row_subject constraint_property target_cells_subject_uri .

        cell_subject_uri a constraint_class .
        cell_subject_uri sh:path cell_value .
        ... (constraint specific statements)

        Applicable to LAM document classes.
    """

    def __init__(self, df: pd.DataFrame,
                 column_mapping_dict: Dict,
                 graph: rdflib.Graph,
                 target_columns: List[str],
                 constraint_property: rdflib.URIRef = SHACL.property,
                 constraint_class: rdflib.URIRef = SHACL.NodeShape,
                 constraint_comment: rdflib.URIRef = SHACL.description,
                 constraint_path_property: rdflib.URIRef = SHACL.path,
                 constraint_value_property: rdflib.URIRef = SHACL.hasValue,
                 constraint_min_property: rdflib.URIRef = SHACL.minCount,
                 constraint_max_property: rdflib.URIRef = SHACL.maxCount,
                 constraint_name_property: rdflib.URIRef = SHACL.name,
                 subject_source_column: str = "URI"):
        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         target_columns=target_columns,
                         subject_source_column=subject_source_column,
                         literal_columns=[],
                         subject_classes=[])
        self.constraint_property = constraint_property
        self.constraint_class = constraint_class
        self.constraint_comment = constraint_comment
        self.constraint_path_property = constraint_path_property
        self.constraint_value_property = constraint_value_property
        self.constraint_min_property = constraint_min_property
        self.constraint_max_property = constraint_max_property
        self.constraint_name_property = constraint_name_property

    def handle_biding_subject(self, row_index, target_column):
        """
        Most of the time biding subject is the row URI however in case of annotations the biding subject is the
        annotated cell subject rather than row subject
        """
        return self.handle_row_uri(row_index=row_index)

    def make_cell_triples(self, row_index, target_column: str) -> List[Tuple]:
        cell_interpretation = self.handle_cell_value(row_index=row_index, target_column=target_column)
        if not cell_interpretation:
            return []
        biding_subject = self.handle_biding_subject(row_index=row_index, target_column=target_column)
        column_predicate = self.handle_column_predicate(target_column=target_column)

        cell_reification_subject = self.handle_cell_reified_subject(row_index=row_index, target_column=target_column)

        result_triples = [(biding_subject, self.constraint_property, cell_reification_subject),
                          (cell_reification_subject, RDF.type, self.constraint_class),
                          (cell_reification_subject, self.constraint_path_property, column_predicate),
                          (cell_reification_subject, DCTERMS.created, rdflib.Literal(date.today()))
                          ]
        # handle values if any
        if VALUES in cell_interpretation:
            result_triples.extend([(cell_reification_subject, self.constraint_value_property, value) for value in
                                   cell_interpretation[VALUES]])

            # also add name and min count when values are provided
            values_as_string_for_comment = ", ".join(cell_interpretation[VALUES])
            result_triples.extend(
                [
                    (cell_reification_subject, self.constraint_min_property,
                     rdflib.Literal("1", datatype=XSD.int)),
                    (cell_reification_subject, SHACL.name,
                     rdflib.Literal(f"Constraint on {column_predicate} to {values_as_string_for_comment}")),
                ])

        # handle min count if any
        if MIN_COUNT in cell_interpretation:
            result_triples.append(
                (cell_reification_subject, self.constraint_min_property,
                 rdflib.Literal(f"{cell_interpretation[MIN_COUNT]}", datatype=XSD.int)))

        # max count values if any
        if MAX_COUNT in cell_interpretation:
            result_triples.append(
                (cell_reification_subject, self.constraint_max_property,
                 rdflib.Literal(f"{cell_interpretation[MAX_COUNT]}", datatype=XSD.int)))

        # comment values if any
        if COMMENT in cell_interpretation:
            result_triples.append(
                (cell_reification_subject, self.constraint_comment,
                 rdflib.Literal(f"{cell_interpretation[COMMENT]}", lang="en")))

        # add name if any available
        if NAME in cell_interpretation:
            result_triples.append(
                (cell_reification_subject, self.constraint_name_property,
                 rdflib.Literal(f"{cell_interpretation[NAME]} {column_predicate}", lang="en")))

        return result_triples

    def handle_cell_reified_subject(self, row_index, target_column: str):
        """
            # also take the cell value into consideration, in case of multi-line cells
            # generating one constraint object for the entire cell rather than for each value in particular
            # this is possible to control by indicating that the constraint object ID is the
            # same for each value because UUID is based on "column + row" rather than "column + row + value"
        :param row_index:
        :param target_column:
        :return:
        """
        return lam_utils.generate_uuid_uri(f"{target_column}-{row_index}",
                                           seed=str(self.df.head()),
                                           graph=self.graph, )


class ConstraintTripleMaker(BaseConstraintTripleMaker):

    def handle_biding_subject(self, row_index, target_column):
        """
        Most of the time biding subject is the row URI however in case of annotations the biding subject is the
        annotated cell subject rather than row subject
        """
        return self.handle_row_uri(row_index=row_index)


class AnnotationConstraintTripleMaker(BaseConstraintTripleMaker):
    """
    Binds the property constraint with the annotation constraint.
    Annotation column mapping is provided from the annotating column to the annotated column.
    This will make only one triple.
    Target  columns should be the annotating columns and the annotated ones are provided in the mapping.
    The column mapping dict must provide formal property mappings to both (a) the annotating columns and
    (b) the annotated columns.
    """

    def __init__(self, df: pd.DataFrame,
                 column_mapping_dict: Dict,
                 graph: rdflib.Graph,
                 annotation_column_mapping: Dict,
                 target_columns: List[str] = [],
                 constraint_property: rdflib.URIRef = SHACL.property,
                 constraint_class: rdflib.URIRef = SHACL.NodeShape,
                 constraint_comment: rdflib.URIRef = SHACL.description,
                 constraint_path_property: rdflib.URIRef = SHACL.path,
                 constraint_value_property: rdflib.URIRef = SHACL.hasValue,
                 constraint_min_property: rdflib.URIRef = SHACL.minCount,
                 constraint_max_property: rdflib.URIRef = SHACL.maxCount,
                 constraint_name_property: rdflib.URIRef = SHACL.name,
                 subject_source_column: str = "URI",
                 ):
        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         target_columns=target_columns,
                         constraint_property=constraint_property,
                         constraint_class=constraint_class,
                         constraint_comment=constraint_comment,
                         constraint_path_property=constraint_path_property,
                         constraint_value_property=constraint_value_property,
                         constraint_min_property=constraint_min_property,
                         constraint_max_property=constraint_max_property,
                         constraint_name_property=constraint_name_property,
                         subject_source_column=subject_source_column)

        self.annotation_column_mapping = annotation_column_mapping

    def handle_biding_subject(self, row_index, target_column):
        return self.handle_cell_reified_subject(row_index=row_index, target_column=self.annotation_column_mapping[
            target_column])

    def make_row_triples(self, row_index, ) -> List[Tuple]:
        return []
