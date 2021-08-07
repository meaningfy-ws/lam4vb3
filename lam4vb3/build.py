"""
builder
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import collections
import warnings
from abc import ABC, abstractmethod
from datetime import date
import pandas as pd
import rdflib
from rdflib.namespace import RDF, SKOS, DCTERMS, XSD

import lam4vb3.cell_parser
from lam4vb3 import lam_utils
from lam4vb3.cell_parser import parse_value, parse_multi_line_value, parse_commented_value, \
    parse_multi_line_commented_value
from lam4vb3.lam_utils import add_triples_to_graph

SHACL = rdflib.Namespace("http://www.w3.org/ns/shacl#")


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

    property_uri = lam4vb3.cell_parser.qname_uri(predicate, graph.namespaces())
    result_triples = []

    for index, subject_uri in subject_index.items():
        result_triples.append(tuple([subject_uri, property_uri, object_index[index]]))

    if inline:
        add_triples_to_graph(result_triples, graph)

    return result_triples


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
                    return lam4vb3.cell_parser.qname_uri(self.df.loc[row_index, self.subject_source], self.graph.namespaces())
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
        return lam4vb3.cell_parser.qname_uri(self.column_mapping_dict[target_column], self.graph.namespaces())

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
        return lam4vb3.cell_parser.qname_lang(self.column_mapping_dict[target_column])

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
            row_subject_class = lam4vb3.cell_parser.qname_uri(self.subject_class, self.graph.namespaces())

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
            row_concept_scheme = lam4vb3.cell_parser.qname_uri(self.subject_in_scheme, self.graph.namespaces())
            result_triples.append(tuple([row_subject, SKOS.inScheme, row_concept_scheme]))
        return result_triples



class ConceptReifiedValueMaker(ConceptTripleMaker):
    """
    TODO: deprecate

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
        reified_value_property_uri = lam4vb3.cell_parser.qname_uri(self.reified_value_property, self.graph.namespaces())
        reified_resource_class_uri = lam4vb3.cell_parser.qname_uri(self.reified_resource_class, self.graph.namespaces())

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
        constraint_property_uri = lam4vb3.cell_parser.qname_uri(self.constraint_property, self.graph.namespaces())
        constraint_class_uri = lam4vb3.cell_parser.qname_uri(self.constraint_class, self.graph.namespaces())
        constraint_comment_uri = lam4vb3.cell_parser.qname_uri(self.constraint_comment, self.graph.namespaces())

        constraint_path_property_uri = lam4vb3.cell_parser.qname_uri(self.constraint_path_property,
                                                                     self.graph.namespaces())

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
        # TODO: deprecate; no longer needed after Excel refactoring

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
            constraint_property_uri = lam4vb3.cell_parser.qname_uri(self.constraint_property, self.graph.namespaces())
            constraint_class_uri = lam4vb3.cell_parser.qname_uri(self.constraint_class, self.graph.namespaces())
            result_triples.extend([tuple([row_subject, constraint_property_uri, target_cells_subject]),
                                   tuple([target_cells_subject, RDF.type, constraint_class_uri]),
                                   tuple([target_cells_subject, SHACL.name,
                                          rdflib.Literal(str(name).strip(), lang="en")]), ])

        return result_triples


