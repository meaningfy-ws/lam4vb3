#!/usr/bin/python3

# base_builders.py
# Date:  04/08/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import collections
import warnings
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

import pandas as pd
import rdflib
from rdflib import RDFS, SKOS

from lam4vb3 import cell_parser
from lam4vb3 import lam_utils


class AbstractTripleMaker(ABC):
    """
        abstract class for building triples from a tabular
    """

    def __init__(self, df: pd.DataFrame,
                 column_mapping_dict: Dict,
                 graph: rdflib.Graph,
                 target_columns: List[str] = [],
                 literal_columns: List[str] = [],
                 subject_source_column: str = "URI",
                 subject_classes: List[rdflib.URIRef] = [RDFS.Resource], ):
        """

        :type subject_classes: state the class subject is an instance of.
        :param df: the source data frame
        :param column_mapping_dict: a dictionary where the keys are data frame columns and the values
                        are qualified URIs used as predicates.
        :param graph: the rdflib graph where namespaces are defined and triples are stored.
        :param target_columns: columns that should be processed by the builder
        :param subject_source_column: can contain (a) a column name to use as subject URIs,
                                (b) if the column does not contain
                                uris then the values are used to generate random URIs (warning, repeated values will
                                lead to generation of the same URI and thus to creation of conflated concepts);
                                (c) if left unspecified, i.e. None, or the column does not exist in the data frame
                                then random URIs are generated based on the row index in the data frame
                                (d) if a list of column names is provided then the URI is generated based on the row index
                                and the list of columns. The list of columns will only be interpreted as a seed string
                                (this means that the list can be with random strings).
        :param literal_columns: names of the columns expected to contain plain literal values
        """

        self.subject_classes: List[rdflib.URIRef] = subject_classes
        self.target_columns: List[str] = target_columns
        self.subject_source_column: str = subject_source_column
        self.literal_columns: List[str] = literal_columns
        self.graph: rdflib.Graph = graph
        self.column_mapping_dict: Dict = column_mapping_dict
        self.df = df
        self._subject_index = None

    def handle_row_uri(self, row_index, seed: str = "") -> rdflib.URIRef:
        """
            generate the row uri based on provided subject_source, which can contain:
            (a) a column name to use as subject URIs,
            (b) if the column does not contain uris then the values are used to generate random URIs (warning,
                repeated values will lead to generation of the same URI and thus to creation of conflated concepts);
            (c) if left unspecified, i.e. None, or the column does not exist in the data frame then random URIs are
                generated based on the row index in the data frame
            (d) if a list of column names is provided then the URI is generated based on the row index
                and the list of columns. The list of columns will only be interpreted as a seed string
            (this means that the list can be with random strings).

        :param seed: an additional seed for random generation
        :param row_index: index of the target row
        :return: rdflib.URIRef
        """

        if self.subject_source_column:
            if isinstance(self.subject_source_column, collections.Iterable) and not isinstance(
                    self.subject_source_column, str):
                return lam_utils.generate_uuid_uri(str(row_index) + str(self.subject_source_column),
                                                   seed=str(self.df.head()) + str(seed),
                                                   graph=self.graph, )

            # if subject source is a column in the DF then make URI of it.
            elif self.subject_source_column in self.df.columns:
                try:
                    # try to parse it as a qualified uri
                    return cell_parser.qname_uri(self.df.loc[row_index, self.subject_source_column],
                                                 self.graph.namespaces())
                except Exception:
                    # if not then dont raise exception but use the values for random generation instead
                    return lam_utils.generate_uuid_uri(self.df.loc[row_index, self.subject_source_column],
                                                       seed=str(self.df.head()) + str(seed),
                                                       graph=self.graph, )

        else:
            return lam_utils.generate_uuid_uri(row_index,
                                               seed=str(self.df.head()) + str(seed),
                                               graph=self.graph, )

    def handle_column_predicate(self, target_column) -> rdflib.URIRef:
        """
            Returns the predicate corresponding to the column, based on the column name.

        :param target_column: string value of a dataframe column title. Resolve from mapping table
        :return: rdflib.URIRef
        """
        return cell_parser.qname_uri(self.column_mapping_dict[target_column], self.graph.namespaces())

    def handle_literal_language_from_predicate_signature(self, target_column) -> str:
        """
            Return the language from the predicate mapping, if any provided;
            this is especially useful when building literal columns.

        :param target_column: string value of a dataframe column title. Resolve from the mapping table.
        :return: str
        """
        return cell_parser.qname_lang(self.column_mapping_dict[target_column])

    def row_uri_index(self) -> dict:
        """
            Builds a dictionary representing the mapping between row index and a URI.
        :return: a dictionary of row index and URI created for the row
        """
        if not self._subject_index:
            self._subject_index = {index: self.handle_row_uri(index)
                                   for (index, row) in self.df.iterrows()}
        return self._subject_index

    def make_triples(self, error_bad_values=True, inplace=True):
        """
            Build the triples for the entire Dataframe

            :param error_bad_values:
            :param inplace:
            :return:
        """

        result_triples = []

        # iterate over the target columns
        for column in self.target_columns:
            try:
                result_triples.extend(self.make_column_triples(target_column=column, ))
            except Exception:
                message = f"Could not create triples for the column {column}."
                if error_bad_values:
                    raise Exception(message)
                else:
                    warnings.warn(message)
                    continue

        # iterate over all the rows
        for index, row in self.df.iterrows():
            try:
                result_triples.extend(self.make_row_triples(row_index=index, ))
            except Exception:
                message = f"Could not create triples for the row {index}."
                if error_bad_values:
                    raise Exception(message)
                else:
                    warnings.warn(message)
                    continue

            # iterate over all the target columns for each row
            for column in self.target_columns:
                try:
                    result_triples.extend(self.make_cell_triples(row_index=index, target_column=column))
                except Exception:
                    message = f"Could not create triples for the cell at row {index} and column {column}."
                    if error_bad_values:
                        raise Exception(message)
                    else:
                        warnings.warn(message)
                        continue

        #  add triples to the graph
        if inplace:
            lam_utils.add_triples_to_graph(result_triples=result_triples, graph=self.graph)

        return result_triples

    def handle_cell_value(self, row_index, target_column: str) -> Dict:
        """
            Parse the cell value

        :param target_column:
        :param row_index:
        :return: parsed cell value
        """
        if target_column in self.literal_columns:
            return cell_parser.parse_cell(cell_value=self.df.loc[row_index, target_column],
                                          is_literal=True,
                                          graph=self.graph)

        return cell_parser.parse_cell(cell_value=self.df.loc[row_index, target_column],
                                      is_literal=True,
                                      graph=self.graph)

    @abstractmethod
    def make_column_triples(self, target_column: str) -> List[Tuple]:
        """
            Build the triples unique to the column
        :param target_column: the column to make triples for
        :return:
        """
        pass

    @abstractmethod
    def make_row_triples(self, row_index, ) -> List[Tuple]:
        """
            Build the triples unique to the row
        :param row_index:
        :return:
        """
        pass

    @abstractmethod
    def make_cell_triples(self, row_index, target_column: str, ) -> List[Tuple]:
        """
            Build cell triples considering the parsed cell value.
        :param row_index:
        :param target_column:
        :return:
        """
        pass


class ConceptTripleMaker(AbstractTripleMaker, ABC):
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
                         subject_classes=subject_classes)

        self.subject_in_scheme = subject_in_scheme
        self.comment_predicate = comment_predicate

    def make_row_triples(self, row_index) -> List[Tuple]:
        result_triples = []  # super().make_row_triples(row_index=row_index)
        if self.subject_in_scheme:
            row_subject = self.handle_row_uri(row_index=row_index, )
            result_triples.append((row_subject, SKOS.inScheme, self.subject_in_scheme))
        return result_triples
