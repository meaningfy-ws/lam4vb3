"""
property_build
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com

This module deals with loading and generating RDF structures for the metadata/property worksheets

"""
import re

import rdflib
from rdflib.namespace import RDF, SKOS, DCTERMS, OWL, XMLNS, XSD
import lam4vb3.build as build
from lam4vb3 import lam_utils

from lam4vb3.lam_utils import qname_uri

LITERAL_COLUMNS = {
    'Code': 'skos:notation',
    'Label': 'skos:prefLabel@en',
    'Definition': 'skos:definition@en',
    'Example - cellar notice': 'skos:example',
    'Analytical methodology': 'skos:scopeNote@en',
    'Specific cases': 'skos:historyNote@en',
    'Comments': 'skos:editorialNote@en',
    'Changes to be done': 'skos:editorialNote@en',
}

URI_COLUMNS = {
    'property': 'sh:path',
}

MULTI_LINE_URI_COLUMNS = {
    'controlled value _property': 'sh:class',
}

COLUMN_ANNOTATION_ASSOCIATIONS = [('annotation_1', 'controlled value_annotation_1'),
                                  ('annotation_2', 'controlled value_annotation_2'),
                                  ('annotation_3', 'controlled value_annotation_3'),
                                  ('annotation_4', 'controlled value_annotation_4'),
                                  ('annotation_5', 'controlled value_annotation_5'),
                                  ('annotation_6', 'controlled value_annotation_6'),
                                  ('annotation_7', 'controlled value_annotation_7'), ]

ANNOTATION_COLUMNS = {
    "annotation_1": "sh:path",
    "controlled value_annotation_1": "sh:class",
    "annotation_2": "sh:path",
    "controlled value_annotation_2": "sh:class",
    "annotation_3": "sh:path",
    "controlled value_annotation_3": "sh:class",
    "annotation_4": "sh:path",
    "controlled value_annotation_4": "sh:class",
    "annotation_5": "sh:path",
    "controlled value_annotation_5": "sh:class",
    "annotation_6": "sh:path",
    "controlled value_annotation_6": "sh:class",
    "annotation_7": "sh:path",
    "controlled value_annotation_7": "sh:class",
}

COLLECTION_COLUMNS = ["Classification level 1", "Classification level 2", "Classification level 3"]

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
    # make literal columns
    literal_maker = build.MultiColumnTripleMaker(df,
                                                 subject_source=URI_COLUMN,
                                                 subject_class="skos:Concept",
                                                 column_mapping_dict=LITERAL_COLUMNS,
                                                 target_columns=list(LITERAL_COLUMNS.keys()),
                                                 uri_valued_columns=[],
                                                 multi_line_columns=[],
                                                 graph=graph)
    literal_maker.make_triples()

    # make uri columns
    uri_maker = build.MultiColumnTripleMaker(df,
                                             subject_source=URI_COLUMN,
                                             subject_class="skos:Concept",
                                             column_mapping_dict=URI_COLUMNS,
                                             target_columns=list(URI_COLUMNS.keys()),
                                             uri_valued_columns=list(URI_COLUMNS.keys()),
                                             multi_line_columns=[],
                                             graph=graph)

    uri_maker.make_triples()

    # make multi line uri columns
    ml_uri_maker = build.MultiColumnTripleMaker(df,
                                                subject_source=URI_COLUMN,
                                                subject_class="skos:Concept",
                                                column_mapping_dict=MULTI_LINE_URI_COLUMNS,
                                                target_columns=list(MULTI_LINE_URI_COLUMNS.keys()),
                                                uri_valued_columns=list(MULTI_LINE_URI_COLUMNS.keys()),
                                                multi_line_columns=list(MULTI_LINE_URI_COLUMNS.keys()),
                                                graph=graph)

    ml_uri_maker.make_triples()

    concept_subject_index = literal_maker.subject_index()
    # go through the annotation columns and build annotation objects and attach them to concept URIs
    for column_pair in COLUMN_ANNOTATION_ASSOCIATIONS:
        annotation_maker1 = build.MultiColumnTripleMaker(df,
                                                         subject_source=None,
                                                         subject_class="lam:PropertyAnnotation",
                                                         column_mapping_dict=ANNOTATION_COLUMNS,
                                                         target_columns=list(column_pair),
                                                         uri_valued_columns=list(column_pair),
                                                         multi_line_columns=[],
                                                         graph=graph)

        ann_subject_index1 = annotation_maker1.subject_index()

        hang_annotation_subjects_on_concept(concept_subject_index=concept_subject_index,
                                            annotation_subject_index=ann_subject_index1,
                                            graph=graph)


def hang_annotation_subjects_on_concept(concept_subject_index, annotation_subject_index,
                                        graph, annotation_property="lam:hasAnnotation", inline=True):
    """
        add triples to the graph connecting concepts to reified annotations
    :return: the resulting triples
    """
    return build.relate_subject_sets(concept_subject_index,
                                     annotation_subject_index,
                                     graph=graph,
                                     predicate=annotation_property,
                                     inline=inline)


def make_property_worksheet(lam_df_properties, prefixes, output_file):
    """
        TODO: work in progress
    :param lam_df_properties:
    :param prefixes:
    :param output_file:
    :return:
    """
    graph = build.make_graph(prefixes)
    create_cs(graph)
    create_concepts(lam_df_properties, graph)
    graph.serialize(str(output_file), format='turtle', )
