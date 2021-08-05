#!/usr/bin/python3

# unused_builders.py
# Date:  04/08/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import uuid
import warnings
from abc import ABC, abstractmethod

import pandas as pd
import rdflib
from rdflib import RDF

import lam4vb3.cell_parser
from lam4vb3 import lam_utils
from lam4vb3.build import PlainTripleMaker
from lam4vb3.lam_utils import add_triples_to_graph
from lam4vb3.cell_parser import parse_multi_line_value, parse_value


class TripleMaker(ABC):
    """
        abstract class for building triples from a tabular
    """

    @abstractmethod
    def handle_subject(self, cell_value) -> rdflib.URIRef:
        """
        :param cell_value: string value of a dataframe cell with subject URI
        :return: rdflib.URIRef
        """

    @abstractmethod
    def handle_predicate(self, column_name) -> rdflib.URIRef:
        """
        :param column_name: string value of a dataframe column title. Resolve from mapping table
        :return: rdflib.URIRef
        """

    @abstractmethod
    def handle_data_type_from_predicate_signature(self, column_name) -> rdflib.URIRef:
        """
        :param column_name: string value of a dataframe column title. Resolve from the mapping table.
        :return: rdflib.URIRef
        """

    @abstractmethod
    def handle_literal_language_from_predicate_signature(self, column_name) -> str:
        """
        :param column_name: string value of a dataframe column title. Resolve from the mapping table.
        :return: str
        """

    @abstractmethod
    def handle_object(self, cell_value):
        """
        :param cell_value: string value of a dataframe cell
        :return: an implementation specific result type
        """

    @abstractmethod
    def make_column_triples(self):
        pass

    @abstractmethod
    def make_cell_triples(self):
        pass


class ColumnTripleMaker(TripleMaker, ABC):
    """
        Create triples in a controlled manned for a specified column.


        Given a target column name present in a descriptive data-frame generate all the RDF triples for the column.
        This functionality is similar to what Sheet2RDF does, and in addition this function allows for multi-level columns,
        which permit specification for additional parameters.

        The rows represent descriptions of LAM concepts. The values in the "URI" column represent
        the concept URIs and function as subjects. The values from the rest of the columns represent
        property values that function as objects. The subject and objects are connected by predicates
        specified in the mapping dictionary from column titles to rdf predicates e.g. {"column title":"predicate", }.

    """

    def __init__(self, df, column_mapping_dict, graph, uri_valued_columns=[], uri_column="URI", multi_line_columns=[]):
        """
            initialise the column triple maker
        :param multi_line_columns: which columns should be considered multiline values or single values
        :param uri_valued_columns: columns whose values are URIs, the rest are considered literals
        :param df: the data frame
        :param column_mapping_dict: the mapping dictionary from column titles to rdf predicates e.g. {"column title":"predicate", }
        """
        self.multi_line_columns = multi_line_columns
        self.uri_valued_columns = uri_valued_columns
        self.df = df
        self.uri_column = uri_column
        self.column_mapping_dict = column_mapping_dict
        self.graph = graph

    def handle_subject(self, cell_value) -> rdflib.URIRef:
        return lam4vb3.cell_parser.qname_uri(cell_value, self.graph.namespaces())

    def handle_predicate(self, column_name) -> rdflib.URIRef:
        return lam4vb3.cell_parser.qname_uri(self.column_mapping_dict[column_name], self.graph.namespaces())

    def handle_data_type_from_predicate_signature(self, column_name) -> rdflib.URIRef:
        """
        :param column_name: string value of a dataframe column title. Resolve from the mapping table.
        :return: rdflib.URIRef
        """
        # TODO: implement something better
        # return XSD.string
        return None

    def handle_literal_language_from_predicate_signature(self, column_name) -> str:
        """
        :param column_name: string value of a dataframe column title. Resolve from the mapping table.
        :return: str
        """
        return lam4vb3.cell_parser.qname_lang(self.column_mapping_dict[column_name])

    def make_column_triples(self, target_column: "the target column",
                            error_bad_lines: "should the bad lines be silently passed or raised as exceptions" = True,
                            inplace: "should the triples be added directly to the graph or returned as a list" = True, ):

        """

        :param inplace: if true the triples are added directly to the graph or,
                        if false returned as a list; the default is true.
        :param target_column: the column to process
        :param error_bad_lines: should the bad lines be silently passed or raised as exceptions
        :return: the set of triples for the entire column
        """
        result_triples = []

        predicate = self.handle_predicate(target_column)
        language = self.handle_literal_language_from_predicate_signature(target_column)
        data_type = self.handle_data_type_from_predicate_signature(target_column)

        if target_column in self.uri_valued_columns and (language or data_type):
            raise Exception(f"The column {target_column} cannot be an column with URIs and, at the same time,"
                            f"have a language tag ({language}) or a data type ({data_type}) in the mapped column property.")

        # create triples for each value in the column
        for quri, obj in zip(self.df[self.uri_column], self.df[target_column]):
            try:
                subject = self.handle_subject(quri)
                oobject = self.handle_object(obj, target_column, language, data_type)

                # if everything went well so far, make the triples
                result_triples.extend(self.make_cell_triples(subject, predicate, oobject))

            except Exception:
                if error_bad_lines:
                    raise Exception(
                        f"Could not create triples for the column {target_column}. "
                        f"There is an error ar the row {quri} and cell value {obj}.")
                else:
                    warnings.warn(
                        f"There is an error ar the row {quri} column {target_column}. The value {obj} was skipped.")
                    continue

        #  add triples to the graph
        if inplace:
            for triple in result_triples:
                self.graph.add(triple)

        return result_triples


class PlainColumnTripleMaker(ColumnTripleMaker):
    """
        for each cell value in a column create triples by parsing the cell value as either a literal
        or as URI, indicated in the constructor which columns shall be considered as a column of URIS
    """

    def handle_object(self, cell_value, target_column, language=None, data_type=None):
        if cell_value and pd.notna(cell_value):
            if target_column in self.multi_line_columns:
                objects = parse_multi_line_value(cell_value,
                                                 graph=self.graph if target_column in self.uri_valued_columns else None,
                                                 language=language,
                                                 data_type=data_type, )
                return [x for x in objects if x]

            return parse_value(cell_value,
                               graph=self.graph if target_column in self.uri_valued_columns else None,
                               language=language,
                               data_type=data_type, )

    def make_cell_triples(self, subject, predicate, oobject):
        """
            for a given subject, predicate, object create the triples gor RDF graph.
            The triple can be simple or reified.
            @return a list of triple tuples
        """
        if isinstance(oobject, list):
            return [tuple([subject, predicate, o]) for o in oobject if o]
        elif oobject:
            return [tuple([subject, predicate, oobject])]
        return []


class ReifiedColumnTripleMaker(ColumnTripleMaker):
    """
        build a set of triples per data frame cell, corresponding to a reified structure

        make
            (s, p, o_uri),
            (o_uri, rdf:type, reification_class),
            (o_uri, reification_property, o),
    """

    def __init__(self, df, column_mapping_dict, graph, uri_column="URI",
                 uri_valued_columns=[],
                 reification_class="skosxl:Label",
                 reification_property="skos:literalForm", ):
        self.reification_class = reification_class
        self.reification_property = reification_property
        super().__init__(df, column_mapping_dict=column_mapping_dict, graph=graph,
                         uri_valued_columns=uri_valued_columns, uri_column=uri_column)

    def handle_object(self, cell_value, target_column, language=None, data_type=None):
        return parse_value(cell_value,
                           graph=self.graph if target_column in self.uri_valued_columns else None,
                           language=language,
                           data_type=data_type, )

    def make_cell_triples(self, subject, predicate, oobject):
        r_class = lam4vb3.cell_parser.qname_uri(self.reification_class, self.graph.namespaces())
        r_property = lam4vb3.cell_parser.qname_uri(self.reification_property, self.graph.namespaces())

        # use the default namespace for intermediary/reification nodes
        r_uri = lam4vb3.cell_parser.qname_uri(":" + str(uuid.uuid4()), self.graph.namespaces())
        return [
            tuple([subject, predicate, r_uri]),
            tuple([r_uri, RDF.type, r_class]),
            tuple([r_uri, r_property, oobject]),
        ]


class MultiColumnTripleMaker(TripleMaker):
    """
        This class facilitates building of the RDF statements based on a data frame.

    """

    def __init__(self, df,
                 column_mapping_dict,
                 graph,
                 target_columns=[],
                 uri_valued_columns=[],
                 subject_source="URI",
                 subject_class="rdfs:Resource",
                 multi_line_columns=[], ):
        """

        :type subject_class: state the class subject is an instance of.
        :param df: the source data frame
        :param column_mapping_dict: a dictionary where the keys are data frame columns and the values
                        are qualified URIs used as predicates.
        :param graph: the rdflib graph where namespaces are defined and triples are stored.
        :param target_columns: columns that should be processed by the builder
        :param subject_source: can contain (a) a column name to use as subject URIs,
                                (b) if the column does not contain
                                uris then the values are used to generate random URIs (warning, repeated values will
                                lead to generation of the same URI and thus to creation of conflated concepts);
                                (c) if left unspecified, i.e. None, or the column does not exist in the data frame
                                then random URIs are generated based on the row index in the data frame
        :param uri_valued_columns: names of the columns expected to contain URI values
        :param multi_line_columns: names of the columns expecting to have multiple lines, and thus shall be interpreted as multi-valued
        """

        self.subject_class = subject_class
        self.target_columns = target_columns
        self.multi_line_columns = multi_line_columns
        self.subject_source = subject_source
        self.uri_valued_columns = uri_valued_columns
        self.graph = graph
        self.column_mapping_dict = column_mapping_dict
        self.df = df
        self._subject_index = None

    def handle_subject(self, row_index, seed="") -> rdflib.URIRef:
        """
        :param seed: an additional seed for random generation
        :param row_index: index of the target row
        :return: rdflib.URIRef
        """
        # if subject source is a column in the DF then make URI of it.
        if self.subject_source in self.df.columns:
            try:
                # try to parse it as a qualified uri
                return lam4vb3.cell_parser.qname_uri(self.df.loc[row_index, self.subject_source], self.graph.namespaces())
            except Exception:
                # if not then dont raise exception but use the values for random generation instead
                return lam_utils.generate_uuid_uri(self.df.loc[row_index, self.subject_source],
                                                   seed=str(self.df.head()) + str(seed),
                                                   graph=self.graph, )

        return lam_utils.generate_uuid_uri(row_index,
                                           seed=str(self.df.head()) + str(seed),
                                           graph=self.graph, )

    def handle_predicate(self, column_name) -> rdflib.URIRef:
        return lam4vb3.cell_parser.qname_uri(self.column_mapping_dict[column_name], self.graph.namespaces())

    def handle_data_type_from_predicate_signature(self, column_name) -> rdflib.URIRef:
        # return XSD.string
        return None

    def handle_literal_language_from_predicate_signature(self, column_name) -> str:
        return lam4vb3.cell_parser.qname_lang(self.column_mapping_dict[column_name])

    def handle_object(self, row_index, target_column, language=None, data_type=None):

        cell_value = self.df.loc[row_index, target_column]

        if cell_value and pd.notna(cell_value):
            if target_column in self.multi_line_columns:
                objects = parse_multi_line_value(cell_value,
                                                 graph=self.graph if target_column in self.uri_valued_columns else None,
                                                 language=language,
                                                 data_type=data_type, )
                return [x for x in objects if x]

            return parse_value(cell_value,
                               graph=self.graph if target_column in self.uri_valued_columns else None,
                               language=language,
                               data_type=data_type, )

    def make_column_triples(self):
        # not useful
        # self.make_triples()
        pass

    def subject_index(self) -> dict:
        """

        :return: a dictionary of row index and subject created for that row
        """
        if not self._subject_index:
            self._subject_index = {index: self.handle_subject(index, seed=str(self.target_columns))
                                   for (index, row) in self.df.iterrows()}
        return self._subject_index

    def make_triples(self, error_bad_lines=True, inplace=True):
        """

        :return:
        """
        result_triples = []
        row_subject_class = lam4vb3.cell_parser.qname_uri(self.subject_class, self.graph.namespaces())
        for index, row in self.df.iterrows():
            row_subject = self.subject_index()[index]  # self.handle_subject(index, seed=str(self.target_columns))

            for column in self.target_columns:
                try:
                    column_predicate = self.handle_predicate(column_name=column)
                    column_data_type = self.handle_data_type_from_predicate_signature(column_name=column)
                    column_language = self.handle_literal_language_from_predicate_signature(column_name=column)
                    _object = self.handle_object(row_index=index,
                                                 target_column=column,
                                                 language=column_language,
                                                 data_type=column_data_type)
                    # if everything is according to the plan, fine
                    result_triples.extend(self.make_cell_triples(row_subject, column_predicate, _object, ))
                    # and also the class statement
                    result_triples.append(tuple([row_subject, RDF.type, row_subject_class]))

                except Exception:
                    if error_bad_lines:
                        raise Exception(
                            f"Could not create triples for the column {column}. "
                            f"There is an error ar the row {index} and cell value: {self.df.loc[index, column]}")
                    else:
                        warnings.warn(
                            f"There is an error ar the row {index} column {column}. "
                            f"Cell value: {self.df.loc[index, column]}")
                        continue

        #  add triples to the graph
        if inplace:
            add_triples_to_graph(result_triples=result_triples, graph=self.graph)

        return result_triples

    def make_cell_triples(self, subject, predicate, oobject):
        """
            for a given subject, predicate, object create the triples gor RDF graph.
            The triple can be simple or reified.
            @return a list of triple tuples
        """
        if isinstance(oobject, list):
            return [tuple([subject, predicate, o]) for o in oobject if o]
        elif oobject:
            return [tuple([subject, predicate, oobject])]
        return []

    def make_row_triples(self):
        pass


class ConceptCollectionMaker(PlainTripleMaker):
    """
        TODO: @Deprecated
        creates from the target columns collections and adds the concept to the last collection.
        The target column list is assumed to represent a sequence of subsumtions where the first
        is the most coarse and the last the most granular collection.
    """

    def __init__(self, df,
                 column_mapping_dict,
                 graph,
                 target_columns=[],
                 subject_source="URI",
                 subject_class="skos:Concept",
                 membership_predicate="skos:member",
                 collection_class="skos:Collectiopn",
                 ):
        """

        :param df:
        :param column_mapping_dict: the collection lexicalisation property
        :param graph:
        :param target_columns: which columns represent collections and in which order
        :param subject_source:
        :param subject_class:
        """
        warnings.warn("deprecated", DeprecationWarning)
        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         target_columns=target_columns,
                         uri_valued_columns=[],
                         subject_source=subject_source,
                         subject_class=subject_class,
                         multi_line_columns=[], )
        self.collection_class = collection_class
        self.membership_predicate = membership_predicate

    def make_cell_triples(self, row_index, target_column):
        """

        :param row_index:
        :param target_column:
        :return:
        """
        return []

    def make_row_triples(self, row_index):
        result_triples = super().make_row_triples(row_index=row_index)

        row_subject = self.handle_row_uri(row_index)

        collection_class_uri = lam4vb3.cell_parser.qname_uri(self.collection_class, self.graph.namespaces())
        membership_predicate_uri = lam4vb3.cell_parser.qname_uri(self.membership_predicate, self.graph.namespaces())

        preceding_subject_uri = None
        for column in self.target_columns:
            cell_values = self.handle_cell_value(row_index=row_index, target_column=column)

            for cell_value in cell_values:
                if cell_value:
                    column_predicate = self.handle_column_predicate(target_column=column)
                    cell_value_subject_uri = lam_utils.generate_uuid_uri(cell_value,
                                                                         seed=str(self.df.head()),
                                                                         graph=self.graph, )

                    result_triples.extend([tuple([cell_value_subject_uri, column_predicate, cell_value]),
                                           tuple([cell_value_subject_uri, RDF.type, collection_class_uri]),
                                           ])

                    if preceding_subject_uri:
                        result_triples.extend(
                            [tuple([preceding_subject_uri, membership_predicate_uri, cell_value_subject_uri]),
                             ])

                    preceding_subject_uri = cell_value_subject_uri

        if preceding_subject_uri:
            result_triples.extend([tuple([preceding_subject_uri, membership_predicate_uri, row_subject]), ])

        return result_triples