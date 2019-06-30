"""
builder
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import rdflib as rdf
import uuid
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, OWL, XMLNS, XSD
from abc import ABC, abstractmethod

import lam4vb3.lam_utils as utils
import pandas as pd
import warnings

# namespace definitions

DCT = DCTERMS
EUVOC = rdf.Namespace("http://publications.europa.eu/ontology/euvoc#")
SKOSXL = rdf.Namespace("http://www.w3.org/2008/05/skos-xl#")
SHACL = rdf.Namespace("http://www.w3.org/ns/shacl#")

CDM = rdf.Namespace("http://publications.europa.eu/ontology/cdm#")
LAM_DATA = rdf.Namespace("http://publications.europa.eu/resources/authority/lam/")
CELEX_DATA = rdf.Namespace("http://publications.europa.eu/resources/authority/celex/")
LAM_SKOS_AP = rdf.Namespace("http://publications.europa.eu/ontology/lam-skos-ap#")


def make_lam_graph():
    """
        init the LAM data graph
    """
    lam_graph = rdf.Graph()

    lam_graph.bind("", LAM_DATA)
    lam_graph.bind("lamd", LAM_DATA)
    lam_graph.bind("celexd", CELEX_DATA)
    lam_graph.bind("lam", LAM_SKOS_AP)

    lam_graph.bind("cdm", CDM)
    lam_graph.bind("euvoc", EUVOC)

    lam_graph.bind("skos", SKOS)
    lam_graph.bind("skosxl", SKOSXL)
    lam_graph.bind("dct", DCTERMS)
    lam_graph.bind("sh", SHACL)

    lam_graph.bind("rdf", RDF)
    lam_graph.bind("rdfs", RDFS)
    lam_graph.bind("xsd", XSD)
    lam_graph.bind("owl", OWL)
    lam_graph.bind("xml", XMLNS)

    return lam_graph


class ColumnTripleMaker(ABC):
    """
        Create triples in a controlled manned  for a specified column.


        Given a target column name present in a descriptive data-frame generate all the RDF triples for the column.
        This functionality is similar to what Sheet2RDF does, and in addition this function allows for multi-level columns,
        which permit specification for additional parameters.

        The rows represent descriptions of LAM concepts. The values in the "URI" column represent
        the concept URIs and function as subjects. The values from the rest of the columns represent
        property values that function as objects. The subject and objects are connected by predicates
        specified in the mapping dictionary from column titles to rdf predicates e.g. {"column title":"predicate", }.

    """

    def __init__(self, df, column_mapping_dict, graph, uri_column="URI"):
        """
            initialise the column triple maker
        :param df: the dataframe
        :param uri_column: the column with uris
        :param column_mapping_dict: the mapping dictionary from column titles to rdf predicates e.g. {"column title":"predicate", }
        """
        self.df = df
        self.uri_column = uri_column
        self.column_mapping_dict = column_mapping_dict
        self.graph = graph

    def make_column_triples(self, target_column: "the target column",
                            is_uri_column: "whether the values are URIs" = False,
                            error_bad_lines: "should the bad lines be silently passed or raised as exceptions" = True):
        """

        :param target_column: the column to process
        :param error_bad_lines: should the bad lines be silently passed or raised as exceptions
        :return: the set of triples for the entire column
        """
        result_triples = []

        predicate = utils.qname_uri(self.column_mapping_dict[target_column], self.graph.namespaces())
        language = utils.qname_lang(self.column_mapping_dict[target_column])

        if is_uri_column and language:
            raise Exception(f"The column {target_column} cannot be an column with URIs and have a language "
                            f"tag @{language} in the mapped column property, which implies literal values.")

        # create triples for each value in the column
        for quri, obj in zip(self.df[self.uri_column], self.df[target_column]):
            # without an uri we cannot do much
            if pd.isna(quri):
                if error_bad_lines:
                    raise Exception("Encountered a row without an URI.")
                else:
                    continue
            # skip nan cells
            if pd.isna(obj):
                continue

            # try to do prepare cell values or fail
            try:
                subject = utils.qname_uri(quri, self.graph.namespaces())

                if is_uri_column:
                    oobject = utils.qname_uri(obj, self.graph.namespaces())
                elif language:
                    oobject = rdf.Literal(obj, lang=self.language)
                else:
                    oobject = rdf.Literal(obj)

                    # if everything went well so far, make the triples
                result_triples.extend(self.make_cell_triples(subject, self.predicate, oobject))
            except Exception:
                if error_bad_lines:
                    raise Exception(
                        f"Could not create triples for the column {target_column}. There is an error ar the row {quri}.")
                else:
                    warnings.warn(
                        f"There is an error ar the row {quri} column {target_column}. The value {obj} was skipped.")
                    continue

    @abstractmethod
    def make_cell_triples(self, subject, predicate, oobject, controled_list_uri):
        """
            for a given subject, predicate, object create the triples gor RDF graph.
            The triple can be simple or reified.
            @return a list of triple tuples
        """
        pass


class SimpleTripleMaker(ColumnTripleMaker):
    """
        make (s,p,o)
    """

    def make_cell_triples(self, subject, predicate, oobject):
        return [tuple([subject, predicate, oobject])]


class ReifiedTripleMaker(ColumnTripleMaker):
    """
        make
            (s, p, o_uri),
            (o_uri, rdf:type, reification_class),
            (o_uri, reification_property, o),
    """

    def __init__(self, df, uri_column, graph, reification_class="skosxl:Label",
                 reification_property="skos:literalForm", ):
        self.reification_class = reification_class
        self.reification_property = reification_property
        super().__init__(df, uri_column, graph, )

    def make_cell_triples(self, subject, predicate, oobject, ):
        r_class = utils.qname_uri(self.reification_class, self.graph.namespaces())
        r_property = utils.qname_uri(self.reification_property, self.graph.namespaces())
        # use the default namespace for intermediary/reification nodes
        r_uri = utils.qname_uri(":" + str(uuid.uuid4()), self.graph.namespaces())
        return [
            tuple([subject, predicate, r_uri]),
            tuple([r_uri, RDF.type, r_class]),
            tuple([r_uri, r_property, oobject]),
        ]
