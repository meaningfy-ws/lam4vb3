"""
builder
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import collections
import re
import uuid
import warnings
from abc import ABC, abstractmethod
from datetime import date
import pandas as pd
import rdflib
from rdflib.namespace import RDF, SKOS, DCTERMS, XSD

from lam4vb3 import lam_utils

SHACL = rdflib.Namespace("http://www.w3.org/ns/shacl#")


def make_graph(df, prefix_column="prefix", uri_column="uri"):
    """
        init the LAM data graph

    :param uri_column: the column in df that contains base namespace URIs
    :param prefix_column: the column in df that provides prefixes to be used in qnames
    :param df: the data frame containing namespace defitions
    """
    graph = rdflib.Graph()

    graph.bind("skos", rdflib.namespace.SKOS)
    graph.bind("dct", rdflib.namespace.DCTERMS)
    graph.bind("sh", SHACL)

    graph.bind("rdf", rdflib.namespace.RDF)
    graph.bind("rdfs", rdflib.namespace.RDFS)
    graph.bind("xsd", rdflib.namespace.XSD)
    graph.bind("owl", rdflib.namespace.OWL)
    graph.bind("xml", rdflib.namespace.XMLNS)

    # normalise the prefixes read into a dataframe
    df.fillna("", inplace=True)
    namespace_mapping_dict = dict(zip(df[prefix_column], df[uri_column]))
    ns_dict = {str(k).replace(":", ""):
                   str(v).strip() if (str(v).endswith("/") or str(v).endswith("#"))
                   else str(str(k) + ":") for k, v in namespace_mapping_dict.items() if v}

    for k, v in ns_dict.items():
        graph.bind(k, rdflib.Namespace(v))

    return graph


def get_subjects_from_triples(resulting_triples):
    """
        provided a list of triples return the list of subjects
    :param resulting_triples:
    :return:
    """
    return list(set([s for s, p, o in resulting_triples]))


def apply_values_to_triple_pattern(values, triple_pattern):
    """
        triple pattern is a list of triple tuples [(s,p,o) , ...]
        values is a list of literals or uris
        for each value the triple pattern is repeated filling in places where the pattern has a None value.

        For example given the triple pattern [(None,rdf:type,skos:Concept)] abd values [:c1, :c2], generate
        [(:C1,rdf:type,skos:Concept), (:c2,rdf:type,skos:Concept)]
    """
    result_triples = []
    for value in values:
        for triple in triple_pattern:
            s, p, o = triple
            new_triple = tuple([s if s is not None else value,
                                p if p is not None else value,
                                o if o is not None else value, ])
            result_triples.append(new_triple)

    return result_triples


def add_triples_to_graph(result_triples, graph):
    """
        just add the triples to a graph
    :return:
    """
    for triple in result_triples:
        graph.add(triple)


def relate_subject_sets(subject_index, object_index, graph, predicate="skos:related", inline=True):
    """
        add triples to the graph connecting concepts to reified annotations
    :param subject_index:
    :param object_index:
    :param predicate:
    :param graph:
    :param inline:
    :return:
    """

    property_uri = lam_utils.qname_uri(predicate, graph.namespaces())
    result_triples = []

    for index, subject_uri in subject_index.items():
        result_triples.append(tuple([subject_uri, property_uri, object_index[index]]))

    if inline:
        add_triples_to_graph(result_triples, graph)

    return result_triples


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
        return lam_utils.qname_uri(cell_value, self.graph.namespaces())

    def handle_predicate(self, column_name) -> rdflib.URIRef:
        return lam_utils.qname_uri(self.column_mapping_dict[column_name], self.graph.namespaces())

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
        return lam_utils.qname_lang(self.column_mapping_dict[column_name])

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
        r_class = lam_utils.qname_uri(self.reification_class, self.graph.namespaces())
        r_property = lam_utils.qname_uri(self.reification_property, self.graph.namespaces())

        # use the default namespace for intermediary/reification nodes
        r_uri = lam_utils.qname_uri(":" + str(uuid.uuid4()), self.graph.namespaces())
        return [
            tuple([subject, predicate, r_uri]),
            tuple([r_uri, RDF.type, r_class]),
            tuple([r_uri, r_property, oobject]),
        ]


# def generate_uri(value, namespace):
#     """
#         strip and replace spaces by dash in the value and then create a uri using the namespace.
#     :param value:
#     :param namespace:
#     :return:
#     """
#     return namespace[str.strip(value).replace(" ", "-")]


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
                return lam_utils.qname_uri(str.strip(value), graph.namespaces())
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
            for x in re.split(r"[\n,]", multi_line_value) if x]


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
    parsed_comment = parse_value(comment, language=language, )
    return parsed_value, parsed_comment


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
                return lam_utils.qname_uri(self.df.loc[row_index, self.subject_source], self.graph.namespaces())
            except Exception:
                # if not then dont raise exception but use the values for random generation instead
                return lam_utils.generate_uuid_uri(self.df.loc[row_index, self.subject_source],
                                                   seed=str(self.df.head()) + str(seed),
                                                   graph=self.graph, )

        return lam_utils.generate_uuid_uri(row_index,
                                           seed=str(self.df.head()) + str(seed),
                                           graph=self.graph, )

    def handle_predicate(self, column_name) -> rdflib.URIRef:
        return lam_utils.qname_uri(self.column_mapping_dict[column_name], self.graph.namespaces())

    def handle_data_type_from_predicate_signature(self, column_name) -> rdflib.URIRef:
        # return XSD.string
        return None

    def handle_literal_language_from_predicate_signature(self, column_name) -> str:
        return lam_utils.qname_lang(self.column_mapping_dict[column_name])

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
        row_subject_class = lam_utils.qname_uri(self.subject_class, self.graph.namespaces())
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


class AbstractTripleMaker(ABC):
    """
        abstract class for building triples from a tabular
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
                                (d) if a list of column names is provided then the URI is generated based on the row index
                                and the list of columns. The list of columns will only be interpreted as a seed string
                                (this means that the list can be with random strings).
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

    def handle_row_uri(self, row_index, seed="") -> rdflib.URIRef:
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

        if self.subject_source:
            if isinstance(self.subject_source, collections.Iterable) and not isinstance(self.subject_source, str):
                return lam_utils.generate_uuid_uri(str(row_index) + str(self.subject_source),
                                                   seed=str(self.df.head()) + str(seed),
                                                   graph=self.graph, )

            # if subject source is a column in the DF then make URI of it.
            elif self.subject_source in self.df.columns:
                try:
                    # try to parse it as a qualified uri
                    return lam_utils.qname_uri(self.df.loc[row_index, self.subject_source], self.graph.namespaces())
                except Exception:
                    # if not then dont raise exception but use the values for random generation instead
                    return lam_utils.generate_uuid_uri(self.df.loc[row_index, self.subject_source],
                                                       seed=str(self.df.head()) + str(seed),
                                                       graph=self.graph, )

        else:
            return lam_utils.generate_uuid_uri(row_index,
                                               seed=str(self.df.head()) + str(seed),
                                               graph=self.graph, )

    def handle_column_predicate(self, target_column) -> rdflib.URIRef:
        """
        :param target_column: string value of a dataframe column title. Resolve from mapping table
        :return: rdflib.URIRef
        """
        return lam_utils.qname_uri(self.column_mapping_dict[target_column], self.graph.namespaces())

    def handle_data_type_from_predicate_signature(self, target_column) -> rdflib.URIRef:
        """
        :param target_column: string value of a dataframe column title. Resolve from the mapping table.
        :return: rdflib.URIRef
        """
        return None

    def handle_literal_language_from_predicate_signature(self, target_column) -> str:
        """
        :param target_column: string value of a dataframe column title. Resolve from the mapping table.
        :return: str
        """
        return lam_utils.qname_lang(self.column_mapping_dict[target_column])

    @abstractmethod
    def handle_cell_value(self, row_index, target_column):
        """
        :param target_column:
        :param row_index:
        :return: parsed cell value
        """

    def row_uri_index(self) -> dict:
        """

        :return: a dictionary of row index and URI created for the row
        """
        if not self._subject_index:
            self._subject_index = {index: self.handle_row_uri(index)
                                   for (index, row) in self.df.iterrows()}
        return self._subject_index

    @abstractmethod
    def make_column_triples(self, target_column):
        """

        :param target_column: the column to make triples for
        :return:
        """
        pass

    @abstractmethod
    def make_row_triples(self, row_index, ):
        pass

    @abstractmethod
    def make_cell_triples(self, row_index, target_column, ):
        pass

    def make_triples(self, error_bad_values=True, inplace=True):
        """

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
                if error_bad_values:
                    raise Exception(
                        f"Could not create triples for the column {column}.")
                else:
                    warnings.warn(f"Could not create triples for the column {column}.")
                    continue

        # iterate over all the rows
        for index, row in self.df.iterrows():
            try:
                result_triples.extend(self.make_row_triples(row_index=index, ))
            except Exception:
                if error_bad_values:
                    raise Exception(
                        f"Could not create triples for the row {index}.")
                else:
                    warnings.warn(f"Could not create triples for the row {index}.")
                    continue
            # iterate over all the target columns for each row
            for column in self.target_columns:
                try:
                    result_triples.extend(self.make_cell_triples(row_index=index, target_column=column))
                except Exception:
                    if error_bad_values:
                        raise Exception(
                            f"Could not create triples for the cell at row {index} and column {column}.")
                    else:
                        warnings.warn(f"Could not create triples for the cell at row {index} and column {column}.")
                        continue

        #  add triples to the graph
        if inplace:
            add_triples_to_graph(result_triples=result_triples, graph=self.graph)

        return result_triples


class PlainTripleMaker(AbstractTripleMaker):
    """
        Builder of resources for each row, column and cell of a data frame.
        The cells are assumed to be simple literals or URIs.
    """

    def __init__(self, df,
                 column_mapping_dict,
                 graph,
                 target_columns=[],
                 uri_valued_columns=[],
                 subject_source="URI",
                 subject_class="rdfs:Resource",
                 multi_line_columns=[],
                 ):

        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         target_columns=target_columns,
                         uri_valued_columns=uri_valued_columns,
                         subject_source=subject_source,
                         subject_class=subject_class,
                         multi_line_columns=multi_line_columns)

    def make_cell_triples(self, row_index, target_column):
        row_subject = self.handle_row_uri(row_index=row_index)
        column_predicate = self.handle_column_predicate(target_column=target_column)

        return [tuple([row_subject, column_predicate, cell_value])
                for cell_value in self.handle_cell_value(row_index, target_column)
                if cell_value]

    def make_row_triples(self, row_index):
        """
             Add class statement for each row subject along with the inScheme and date of creation.
             If the target cells are empty don't produce any row triples.

        :param row_index:
        :return:
        """
        # if any cells has values make the row triples otherwise skip teh row triples
        if not self.df.loc[row_index, self.target_columns].isnull().values.all():
            row_subject_class = lam_utils.qname_uri(self.subject_class, self.graph.namespaces())

            row_subject = self.handle_row_uri(row_index=row_index, )

            return [tuple([row_subject, RDF.type, row_subject_class]),
                    tuple([row_subject, DCTERMS.created, rdflib.Literal(date.today())]), ]
        return []

    def make_column_triples(self, target_column):
        """
            not much use for his function in most of the use cases
        :param target_column:
        :return:
        """
        return []

    def handle_cell_value(self, row_index, target_column) -> list:
        """
            Return the list of values resulting from parsing the data sheet cell.
            Most of the time it is a single or no value.

        :param row_index:
        :param target_column:
        :return:
        """
        data_type = self.handle_data_type_from_predicate_signature(target_column=target_column)
        language = self.handle_literal_language_from_predicate_signature(target_column=target_column)

        cell_value = self.df.loc[row_index, target_column]

        if cell_value and pd.notna(cell_value):
            if target_column in self.multi_line_columns:
                objects = parse_multi_line_value(cell_value,
                                                 graph=self.graph if target_column in self.uri_valued_columns else None,
                                                 language=language,
                                                 data_type=data_type, )
                return [x for x in objects if x]

            return [parse_value(cell_value,
                                graph=self.graph if target_column in self.uri_valued_columns else None,
                                language=language,
                                data_type=data_type, )]
        return []


class InverseTripleMaker(AbstractTripleMaker):
    """
        Builds triples from columns (which must contain URI references) to the row URI.
        The cells are assumed to be always URIs.
    """

    def __init__(self, df,
                 column_mapping_dict,
                 graph,
                 target_columns=[],
                 subject_source="URI",
                 ):
        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         target_columns=target_columns,
                         uri_valued_columns=target_columns,
                         subject_source=subject_source,
                         subject_class="rdfs:Resource",
                         multi_line_columns=[])

    def make_column_triples(self, target_column):
        return []

    def make_row_triples(self, row_index):
        return []

    def make_cell_triples(self, row_index, target_column):
        row_subject = self.handle_row_uri(row_index=row_index)
        column_predicate = self.handle_column_predicate(target_column=target_column)

        return [tuple([cell_value, column_predicate, row_subject])
                for cell_value in self.handle_cell_value(row_index, target_column)
                if cell_value]

    def handle_cell_value(self, row_index, target_column):
        cell_value = self.df.loc[row_index, target_column]
        if cell_value and pd.notna(cell_value):
            return [parse_value(cell_value,
                                graph=self.graph,
                                language=None,
                                data_type=None, )]
        return []


class ConceptTripleMaker(PlainTripleMaker):
    """
        Creates literals/uri statements from cell values attached to a concept using the following pattern

        row_subject a subject_class .
        row_subject column_predicate cell_value .
    """

    def __init__(self, df,
                 column_mapping_dict,
                 graph,
                 subject_in_scheme=None,
                 target_columns=[],
                 uri_valued_columns=[],
                 subject_source="URI",
                 subject_class="skos:Concept",
                 multi_line_columns=[], ):
        """

        :param subject_in_scheme: the concept scheme hosting the subject concept. Can also be None
        """
        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         target_columns=target_columns,
                         uri_valued_columns=uri_valued_columns,
                         subject_source=subject_source,
                         subject_class=subject_class,
                         multi_line_columns=multi_line_columns)

        self.subject_in_scheme = subject_in_scheme

    def make_row_triples(self, row_index):
        result_triples = super().make_row_triples(row_index=row_index)
        if self.subject_in_scheme:
            row_subject = self.handle_row_uri(row_index=row_index, )
            row_concept_scheme = lam_utils.qname_uri(self.subject_in_scheme, self.graph.namespaces())
            result_triples.append(tuple([row_subject, SKOS.inScheme, row_concept_scheme]))
        return result_triples


class ConceptReifiedValueMaker(ConceptTripleMaker):
    """
        Creates reified literals/uri from cell values attached to a concept using the following pattern

        row_subject a subject_class .
        row_subject column_predicate cell_subject_uri .
        cell_subject_uri a reified_resource_class .
        cell_subject_uri reified_value_property cell_value .
    """

    def __init__(self, df,
                 column_mapping_dict,
                 graph,
                 subject_in_scheme,
                 reified_value_property="rdf:value",
                 reified_resource_class="rdfs:Resource",
                 target_columns=[],
                 uri_valued_columns=[],
                 subject_source="URI",
                 subject_class="skos:Concept",
                 multi_line_columns=[], ):
        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         subject_in_scheme=subject_in_scheme,
                         target_columns=target_columns,
                         uri_valued_columns=uri_valued_columns,
                         subject_source=subject_source,
                         subject_class=subject_class,
                         multi_line_columns=multi_line_columns)

        self.reified_resource_class = reified_resource_class
        self.reified_value_property = reified_value_property

    def make_cell_triples(self, row_index, target_column):
        row_subject = self.handle_row_uri(row_index=row_index)
        column_predicate = self.handle_column_predicate(target_column=target_column)
        reified_value_property_uri = lam_utils.qname_uri(self.reified_value_property, self.graph.namespaces())
        reified_resource_class_uri = lam_utils.qname_uri(self.reified_resource_class, self.graph.namespaces())

        result_triples = []

        cell_values = self.handle_cell_value(row_index, target_column)
        if cell_values:
            for cell_value in cell_values:
                if cell_value:
                    cell_subject = lam_utils.generate_uuid_uri(
                        str(target_column) + str(row_index) + str(cell_value),
                        seed=str(self.df.head()),
                        graph=self.graph, )

                    result_triples.extend([
                        tuple([row_subject, column_predicate, cell_subject]),
                        tuple([cell_subject, RDF.type, reified_resource_class_uri]),
                        tuple([cell_subject, reified_value_property_uri, cell_value]),

                    ])

        return result_triples


class ConceptConstraintMaker(ConceptTripleMaker):
    """
        Creates constraint objects from cell values (once cell one constraint) attached to a concept using the following pattern

        row_subject a subject_class .
        row_subject constraint_property target_cells_subject_uri .

        cell_subject_uri a constraint_class .
        cell_subject_uri sh:path cell_value .
        ... (constraint specific statements)

        Applicable to LAM document classes.
    """

    def __init__(self, df,
                 column_mapping_dict,
                 graph,
                 subject_in_scheme,
                 constraint_property="lam:hasPropertyConfiguration",
                 constraint_class="sh:PropertyShape",
                 constraint_comment="skos:editorialNote",
                 constraint_path_property="sh:path",
                 target_columns=[],
                 uri_valued_columns=[],
                 subject_source="URI",
                 subject_class="skos:Concept",
                 multi_line_columns=[], ):
        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         subject_in_scheme=subject_in_scheme,
                         target_columns=target_columns,
                         uri_valued_columns=uri_valued_columns,
                         subject_source=subject_source,
                         subject_class=subject_class,
                         multi_line_columns=multi_line_columns)
        self.constraint_path_property = constraint_path_property
        self.constraint_comment = constraint_comment
        self.constraint_class = constraint_class
        self.constraint_property = constraint_property

    def handle_cell_value(self, row_index, target_column) -> list:
        cell_value = self.df.loc[row_index, target_column]
        graph = self.graph if target_column in self.uri_valued_columns else None
        language = self.handle_literal_language_from_predicate_signature(target_column=target_column)
        data_type = self.handle_data_type_from_predicate_signature(target_column=target_column)

        if cell_value and pd.notna(cell_value):
            if target_column in self.multi_line_columns:
                objects = parse_multi_line_commented_value(cell_value,
                                                           graph=graph,
                                                           language=language,
                                                           data_type=data_type, )
                return [x for x in objects if x]

            return [parse_commented_value(cell_value,
                                          graph=graph,
                                          language=language,
                                          data_type=data_type, )]
        return []

    def make_cell_triples(self, row_index, target_column):
        row_subject = self.handle_row_uri(row_index=row_index)
        column_predicate = self.handle_column_predicate(target_column=target_column)
        constraint_property_uri = lam_utils.qname_uri(self.constraint_property, self.graph.namespaces())
        constraint_class_uri = lam_utils.qname_uri(self.constraint_class, self.graph.namespaces())
        constraint_comment_uri = lam_utils.qname_uri(self.constraint_comment, self.graph.namespaces())

        constraint_path_property_uri = lam_utils.qname_uri(self.constraint_path_property, self.graph.namespaces())

        result_triples = []

        cell_values = self.handle_cell_value(row_index, target_column)

        if cell_values:
            for cell_value, cell_comment in cell_values:
                if cell_value or cell_comment:

                    # if only a single cell value is available then use the ["column"] as source of uri.
                    # it should be the list with a single element, the column name, to be compatible with
                    # default uri handler.
                    if len(cell_values) == 1:
                        cell_subject = lam_utils.generate_uuid_uri(str(row_index) + str(target_column),
                                                                   seed=str(self.df.head()),
                                                                   graph=self.graph, )
                    else:  # also take the cell value into consideration, in case of multi-line cells
                        # generating one constraint object for the entire cell rather than for each value in particular
                        # this is possible to control by indicating that the constraint object ID is the
                        # same for each value because UUID is based on "column + row" rather than "column + row + value"
                        cell_subject = lam_utils.generate_uuid_uri(
                            str(target_column) + str(row_index),  # + str(cell_value) + str(cell_comment)
                            seed=str(self.df.head()),
                            graph=self.graph, )

                    result_triples.extend([tuple([row_subject, constraint_property_uri, cell_subject]),
                                           tuple([cell_subject, RDF.type, constraint_class_uri]),
                                           tuple([cell_subject, constraint_path_property_uri, column_predicate]),
                                           ])
                    if cell_comment:
                        result_triples.append(tuple([cell_subject, constraint_comment_uri, cell_comment]))

                    # the qualified name of the property for human friendly view
                    predicate = self.graph.qname(column_predicate)

                    if str(cell_value).strip().lower() == "y":
                        result_triples.extend([
                            tuple([cell_subject, SHACL.name, rdflib.Literal(f"Mandatory {predicate}")]),
                            tuple([cell_subject, SHACL.minCount, rdflib.Literal("1", datatype=XSD.int)]),
                        ])
                    elif str(cell_value).strip().lower() == "yu":
                        result_triples.extend([
                            tuple([cell_subject, SHACL.name, rdflib.Literal(f"Mandatory unique {predicate}")]),
                            tuple([cell_subject, SHACL.minCount, rdflib.Literal("1", datatype=XSD.int)]),
                            tuple([cell_subject, SHACL.maxCount, rdflib.Literal("1", datatype=XSD.int)]),
                        ])
                    elif str(cell_value).strip().lower() == "o":
                        result_triples.extend([
                            tuple([cell_subject, SHACL.name, rdflib.Literal(f"Optional {predicate} ")]),
                        ])
                    elif str(cell_value).strip().lower() == "ou":
                        result_triples.extend([
                            tuple([cell_subject, SHACL.name, rdflib.Literal(f"Optional unique {predicate}")]),
                            tuple([cell_subject, SHACL.maxCount, rdflib.Literal("1", datatype=XSD.int)]),
                        ])
                    elif str(cell_value).strip().lower() == "n":
                        result_triples.extend([
                            tuple([cell_subject, SHACL.name, rdflib.Literal(f"Forbidden {predicate}")]),
                            tuple([cell_subject, SHACL.maxCount, rdflib.Literal("0", datatype=XSD.int)]),
                        ])
                    else:
                        if target_column in self.uri_valued_columns:
                            try:
                                cell_value_string = self.graph.qname(cell_value)
                            except ValueError:
                                # silently failing to parse a URI and providing the value as literal instead
                                cell_value_string = str(cell_value)
                        else:
                            cell_value_string = str(cell_value)
                        result_triples.extend([
                            tuple([cell_subject, SHACL.minCount, rdflib.Literal("1", datatype=XSD.int)]),
                            tuple([cell_subject, SHACL.value, cell_value]),
                            tuple([cell_subject, SHACL.name,
                                   rdflib.Literal(f"Constraint on {predicate} to {cell_value_string}")]),
                        ])

        return result_triples


class ConceptMultiColumnConstraintMaker(PlainTripleMaker):
    """
        creates an object from the cells of the target columns and attach it to the row id uri.

        row_subject a subject_class .
        row_subject constraint_property target_cells_subject_uri .

        target_cells_subject_uri a constraint_class .
        ...
        target_cells_subject_uri column_predicate cell_value .
        ...

    """

    def __init__(self, df,
                 column_mapping_dict,
                 graph,
                 target_columns=[],
                 uri_valued_columns=[],
                 subject_source="URI",
                 subject_class="rdfs:Resource",
                 multi_line_columns=[],
                 constraint_property="lam:hasAnnotationConfiguration",
                 constraint_class="lam:AnnotationConfiguration",
                 ):
        super().__init__(df=df,
                         column_mapping_dict=column_mapping_dict,
                         graph=graph,
                         target_columns=target_columns,
                         uri_valued_columns=uri_valued_columns,
                         subject_source=subject_source,
                         subject_class=subject_class,
                         multi_line_columns=multi_line_columns,
                         )
        self.constraint_class = constraint_class
        self.constraint_property = constraint_property

    def make_cell_triples(self, row_index, target_column):
        """

        :param row_index:
        :param target_column:
        :return:
        """
        return []

    def make_row_triples(self, row_index):
        """
            create a new object and add the set of triples based on the row id and target columns
        :param row_index:
        :return:
        """

        result_triples = []
        name = "Annotated with "

        row_subject = self.handle_row_uri(row_index)

        # target_cells_subject = self.handle_row_uri(row_index, seed=str(self.target_columns))
        target_cells_subject = lam_utils.generate_uuid_uri(str(row_index) + str(self.target_columns),
                                                           seed=str(self.df.head()),
                                                           graph=self.graph, )

        for column in self.target_columns:
            column_predicate = self.handle_column_predicate(target_column=column)
            cell_values = self.handle_cell_value(row_index=row_index, target_column=column)

            for cell_value in cell_values:
                if cell_value:
                    name += str(self.graph.qname(cell_value)) + " "
                    result_triples.extend([tuple([target_cells_subject, column_predicate, cell_value]),
                                           tuple([target_cells_subject, SHACL.minCount,
                                                  rdflib.Literal("1", datatype=XSD.int)]),
                                           ])

        if result_triples:
            result_triples.extend(super().make_row_triples(row_index=row_index))
            constraint_property_uri = lam_utils.qname_uri(self.constraint_property, self.graph.namespaces())
            constraint_class_uri = lam_utils.qname_uri(self.constraint_class, self.graph.namespaces())
            result_triples.extend([tuple([row_subject, constraint_property_uri, target_cells_subject]),
                                   tuple([target_cells_subject, RDF.type, constraint_class_uri]),
                                   tuple([target_cells_subject, SHACL.name,
                                          rdflib.Literal(str(name).strip(), lang="en")]), ])

        return result_triples


class ConceptCollectionMaker(PlainTripleMaker):
    """
        @Deprecated
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

        collection_class_uri = lam_utils.qname_uri(self.collection_class, self.graph.namespaces())
        membership_predicate_uri = lam_utils.qname_uri(self.membership_predicate, self.graph.namespaces())

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
