"""
property_build
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com

This module deals with loading and generating RDF structures for the metadata/property worksheets

"""

import rdflib
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, OWL, XMLNS, XSD
import lam4vb3.build as build

# Mapping LAM and CELEX metadata worksheet columns¶ (LAM and CELEX have identical property definitions)
from lam4vb3.lam_utils import qname_uri

LAM_PROPERTIES_DESCRIPTIVE_COLUMNS = {
    'Code': 'skos:notation',
    'Label': 'skos:prefLabel@en',
    'property': 'sh:path',
    'controlled value _property': 'sh:class',
    'Definition': 'skos:definition@en',
    'Example - cellar notice': 'skos:example',
    'Analytical methodology': 'skos:scopeNote@en',
    'Specific cases': 'skos:historyNote@en',
    'Comments': 'skos:editorialNote@en',
    'Changes to be done': 'skos:editorialNote@en',
}

URI_VALUED_COLUMNS = ['property', 'controlled value _property']

LAM_PROPERTIES_ANNOTATION_COLUMNS = [('annotation_1', 'controlled value_annotation_1'),
                                     ('annotation_2', 'controlled value_annotation_2'),
                                     ('annotation_3', 'controlled value_annotation_3'),
                                     ('annotation_4', 'controlled value_annotation_4'),
                                     ('annotation_5', 'controlled value_annotation_5'),
                                     ('annotation_6', 'controlled value_annotation_6'),
                                     ('annotation_7', 'controlled value_annotation_7'), ]

LAM_COLLECTION_COLUMNS = ["Classification level 1", "Classification level 2", "Classification level 3"]

LAM_MD_CS = rdflib.URIRef("http://publications.europa.eu/resources/authority/lam-metadata")
# a little bit of column management
URI_COLUMN = 'URI'


def create_cs(graph):
    """
        create the concept scheme definition
    """
    graph.add((LAM_MD_CS, RDF.type, SKOS.ConceptScheme))
    graph.add((LAM_MD_CS, SKOS.prefLabel, rdflib.Literal("Document metadata")))


def create_concepts(df, graph):
    """
        for each row create triples for all descriptive columns.
    """
    for idx, row in df.iterrows():
        subject = qname_uri(row[URI_COLUMN], graph.namespaces())
        graph.add((subject, RDF.type, SKOS.Concept))
        graph.add((subject, SKOS.topConceptOf, LAM_MD_CS))  # supposed to be skos:inScheme

        # add descriptive triples with URI values for each column
        simple_uri_maker = build.ColumnTripleMaker(df,
                                                   uri_column=URI_COLUMN,
                                                   column_mapping_dict=LAM_PROPERTIES_DESCRIPTIVE_COLUMNS,
                                                   uri_valued_columns=URI_VALUED_COLUMNS,
                                                   graph=graph)
        for column_name in LAM_PROPERTIES_DESCRIPTIVE_COLUMNS.keys():
            simple_uri_maker.make_column_triples(target_column=column_name)
