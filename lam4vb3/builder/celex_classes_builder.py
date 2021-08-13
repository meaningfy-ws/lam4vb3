#!/usr/bin/python3

# property_builder.py
# Date:  05/08/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com

""" """
import rdflib
from rdflib import SKOS, RDF

import lam4vb3.lam_utils
from lam4vb3.builder import LAM, CELEXD
from lam4vb3.builder.inverse_builders import InverseTripleMaker
from lam4vb3.builder.simple_builders import ConceptTripleMaker, SimpleTripleMaker

LITERAL_CONCEPTS_COLUMNS = {
    'CODE': 'skos:notation',
    'LABEL': 'skos:prefLabel@en'
}

LITERAL_COLLECTIONS_COLUMNS = {
    'CODE': 'skos:notation',
    'LABEL': 'skos:prefLabel@en',
    'DESCRIPTION': 'skos:description',
    'COMMENT': 'skos:editorialNote@en',
    'ORDER': 'euvoc:order'
}

URI_COLLECTIONS_COLUMNS = {
    'PARENT_COLLECTION': 'skos:member',
}

PARENT_CONCEPT_COLUMN = {'PARENT': 'skos:broader'}

COLLECTION_COLUMNS = {"CLASSIFICATION": "skos:member"}

LAM_CS = CELEXD.CelexClasses

URI_COLUMN = 'URI'


def create_concept_scheme(graph):
    """
        create the concept scheme definition
    """
    graph.add((LAM_CS, RDF.type, SKOS.ConceptScheme))
    graph.add((LAM_CS, SKOS.prefLabel, rdflib.Literal("Legal Document")))


def create_concepts(df, graph):
    concept_maker = ConceptTripleMaker(df=df,
                                       column_mapping_dict=LITERAL_CONCEPTS_COLUMNS,
                                       graph=graph,
                                       subject_in_scheme=LAM_CS,
                                       comment_predicate=SKOS.editorialNote,
                                       target_columns=[*LITERAL_CONCEPTS_COLUMNS],
                                       literal_columns=[*LITERAL_CONCEPTS_COLUMNS],
                                       subject_source_column=URI_COLUMN,
                                       subject_classes=[SKOS.Concept, LAM.LegalDocumentClass])  #changed from LAMD to LAM

    concept_maker.make_triples()

    in_collection_maker = InverseTripleMaker(df=df,
                                             column_mapping_dict=COLLECTION_COLUMNS,
                                             graph=graph,
                                             target_columns=[*COLLECTION_COLUMNS],
                                             subject_source_column=URI_COLUMN
                                             )

    in_collection_maker.make_triples()

    parent_concept_maker = InverseTripleMaker(df=df,
                                              column_mapping_dict=PARENT_CONCEPT_COLUMN,
                                              graph=graph,
                                              target_columns=[*PARENT_CONCEPT_COLUMN],
                                              subject_source_column=URI_COLUMN
                                              )

    parent_concept_maker.make_triples()


def create_collections(df, graph):
    selected_columns = {**LITERAL_COLLECTIONS_COLUMNS,
                        **URI_COLLECTIONS_COLUMNS}
    collection_maker = SimpleTripleMaker(df=df,
                                         column_mapping_dict=selected_columns,
                                         graph=graph,
                                         target_columns=[*selected_columns],
                                         literal_columns=[*LITERAL_COLLECTIONS_COLUMNS],
                                         subject_source_column=URI_COLUMN,
                                         subject_classes=[SKOS.Collection],
                                         comment_predicate=SKOS.editorialNote)
    collection_maker.make_triples()

    collection_parent_maker = InverseTripleMaker(df=df,
                                                 column_mapping_dict=URI_COLLECTIONS_COLUMNS,
                                                 graph=graph,
                                                 target_columns=[*URI_COLLECTIONS_COLUMNS],
                                                 subject_source_column=URI_COLUMN
                                                 )

    collection_parent_maker.make_triples()


def make_celex_classes_worksheet(lam_df_celex_classes, lam_df_celex_classes_classification, prefixes, output_file):
    """
    :param lam_df_celex_classes_classification:
    :param lam_df_celex_classes:
    :param prefixes:
    :param output_file:
    :return:
    """
    graph = lam4vb3.lam_utils.make_graph(prefixes)
    create_concept_scheme(graph)
    create_concepts(lam_df_celex_classes, graph)
    create_collections(lam_df_celex_classes_classification, graph)
    graph.serialize(str(output_file), format='turtle', )
    return graph
