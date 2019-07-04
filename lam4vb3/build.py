"""
builder
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import re

import rdflib
# import rdflib as rdf
import uuid
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, OWL, XMLNS, XSD
from abc import ABC, abstractmethod

import lam4vb3.lam_utils as utils
import pandas as pd
import warnings


def make_graph(df, prefix_column="prefix", uri_column="uri"):
    """
        init the LAM data graph
    """
    graph = rdflib.Graph()

    graph.bind("skos", rdflib.namespace.SKOS)
    graph.bind("dct", rdflib.namespace.DCTERMS)

    graph.bind("rdf", rdflib.namespace.RDF)
    graph.bind("rdfs", rdflib.namespace.RDFS)
    graph.bind("xsd", rdflib.namespace.XSD)
    graph.bind("owl", rdflib.namespace.OWL)
    graph.bind("xml", rdflib.namespace.XMLNS)

    # normalise the prefixes read into a dataframe
    namespace_mapping_dict = dict(zip(df[prefix_column], df[uri_column]))
    ns_dict = {str(k).replace(":", ""):
                   str(v).strip() if (str(v).endswith("/") or str(v).endswith("#"))
                   else str(str(k) + ":") for k, v in namespace_mapping_dict.items() if k and v}

    for k, v in ns_dict.items():
        graph.bind(k, rdflib.Namespace(v))

    return graph


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
        :param uri_column: the column with uris
        :param column_mapping_dict: the mapping dictionary from column titles to rdf predicates e.g. {"column title":"predicate", }
        """
        self.multi_line_columns = multi_line_columns
        self.uri_valued_columns = uri_valued_columns
        self.df = df
        self.uri_column = uri_column
        self.column_mapping_dict = column_mapping_dict
        self.graph = graph

    def handle_subject(self, cell_value) -> rdflib.URIRef:
        return utils.qname_uri(cell_value, self.graph.namespaces())

    def handle_predicate(self, column_name) -> rdflib.URIRef:
        return utils.qname_uri(self.column_mapping_dict[column_name], self.graph.namespaces())

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
        return utils.qname_lang(self.column_mapping_dict[column_name])

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
        r_class = utils.qname_uri(self.reification_class, self.graph.namespaces())
        r_property = utils.qname_uri(self.reification_property, self.graph.namespaces())

        # use the default namespace for intermediary/reification nodes
        r_uri = utils.qname_uri(":" + str(uuid.uuid4()), self.graph.namespaces())
        return [
            tuple([subject, predicate, r_uri]),
            tuple([r_uri, RDF.type, r_class]),
            tuple([r_uri, r_property, oobject]),
        ]


def generate_uri(value, namespace):
    """
        strip and replace spaces by dash in the value and then create a uri using the namespace.
    :param value:
    :param namespace:
    :return:
    """
    return namespace[str.strip(value).replace(" ", "-")]


def parse_value(value, graph=None, language=None, data_type=None):
    """
        create a resource either as URI or Literal
    :param value:
    :param graph:
    :param language:
    :param data_type:
    :return: URIRef or Literal
    """
    if value and not pd.isna(value):
        if graph is not None:
            try:
                return utils.qname_uri(str.strip(value), graph.namespaces())
            except Exception:
                return rdflib.URIRef(str.strip(value))
        elif language:
            return rdflib.Literal(value, lang=language)
        elif data_type:
            return rdflib.Literal(value, datatype=data_type)
        else:
            return rdflib.Literal(value)


def parse_multi_line_value(multi_line_value, graph=None, language=None, data_type=None):
    """

    :param multi_line_value:
    :param graph:
    :param language:
    :param data_type:
    :return:
    """
    return [parse_value(x, graph=graph, language=language, data_type=data_type)
            for x in re.split(r"\n", multi_line_value) if x]


def parse_commented_value(commented_value, graph=None, language=None, data_type=None) -> (
        "cell value", "cell comment"):
    """
        return the tuple (value,comment) spiting the cell_value into the actual value and the comment,
        which is the part after the special character pipe (|) or tilda (~). If no comment is provided None is returned

        examples:
            value1 | with a comment
            value2 ~ with another comment

    :param data_type:
    :param language:
    :param graph: should the value be interpreted as URI, then use this graph for name space intepretation
    :param commented_value: the string value of the cell
    :return: tuple("cell value", "cell comment")
    """
    parts = [x for x in re.split(r"[~\|]", commented_value) if x]
    value = parts[0] if parts else None
    comment = parts[1] if len(parts) > 1 else None
    parsed_value = parse_value(value, graph=graph, language=language, data_type=data_type)
    return parsed_value, comment


def parse_multi_line_commented_value(multi_line_commented_value, graph=None, language=None,
                                     data_type=None) -> [("cell value", "cell comment")]:
    """
        return a list of tuples where each tuple is a (value,comment) split
    :param multi_line_commented_value:
    :param graph:
    :param language:
    :param data_type:
    :return:
    """

    lines = [str.strip(x) for x in re.split(r"\n", multi_line_commented_value) if x]
    return [parse_commented_value(x, graph=graph, language=language, data_type=data_type) for x in lines
            if x]
