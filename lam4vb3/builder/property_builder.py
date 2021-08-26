#!/usr/bin/python3

# property_builder.py
# Date:  05/08/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import rdflib
from rdflib import SKOS, RDF

import lam4vb3.lam_utils
from lam4vb3.builder import LAM, LAMD, SHACL
from lam4vb3.builder.inverse_builders import InverseTripleMaker
from lam4vb3.builder.reified_builders import ConstraintTripleMaker
from lam4vb3.builder.simple_builders import ConceptTripleMaker, SimpleTripleMaker

LITERAL_CONCEPTS_COLUMNS = {
    'CODE': 'skos:notation',
    'LABEL': 'skos:prefLabel@en',
    'DESCRIPTION': 'skos:definition',
    'Example - cellar notice': 'skos:example',
    'Example - EUR-Lex display notice': 'skos:example',
    'Example - EUR-Lex index notice': 'skos:example',
    'Analytical methodology': 'skos:scopeNote@en',
    'Specific cases': 'skos:historyNote@en',
    'Comments': 'skos:editorialNote@en',
    'PROP_TYPE': 'dct:type'
}

LITERAL_COLLECTIONS_COLUMNS = {
    'CODE': 'skos:notation',
    'LABEL': 'skos:prefLabel@en',
    'DESCRIPTION': 'skos:definition',
    'COMMENT': 'skos:editorialNote@en',
    'ORDER': 'euvoc:order'
}

URI_CONCEPTS_COLUMNS = {
    'SH_PATH': 'sh:path',
    'CONTROLLED_LIST': 'sh:class'
}

URI_COLLECTIONS_COLUMNS = {
    'PARENT_COLLECTION': 'skos:member',
}

CONSTRAINT_COLUMNS = {
    'ANN_COD': 'lamd:md_ANN_COD',
    'ANN_TOD': 'lamd:md_ANN_TOD',
    'ANN_ART': 'lamd:md_ANN_ART',
    'ANN_CLB': 'lamd:md_ANN_CLB',
    'ANN_FCS': 'lamd:md_ANN_FCS',
    'ANN_FCT': 'lamd:md_ANN_FCT',
    'ANN_TLT': 'lamd:md_ANN_TLT',
    'ANN_PAR': 'lamd:md_ANN_PAR',
    'ANN_RL2': 'lamd:md_ANN_RL2',
    'ANN_MDL': 'lamd:md_ANN_MDL',
    'ANN_SOV': 'lamd:md_ANN_SOV',
    'ANN_SUB': 'lamd:md_ANN_SUB',
    'ANN_MSL': 'lamd:md_ANN_MSL',
    'ANN_EOV': 'lamd:md_ANN_EOV',
    'ANN_LVL': 'lamd:md_ANN_LVL',
}

COLLECTION_COLUMNS = {"CLASSIFICATION": "skos:member"}

LAM_CS = LAMD.LAMProperties

URI_COLUMN = 'URI'


def create_concept_scheme(graph):
    """
        create the concept scheme definition
    """
    graph.add((LAM_CS, RDF.type, SKOS.ConceptScheme))
    graph.add((LAM_CS, SKOS.prefLabel, rdflib.Literal("Document properties")))


def create_concepts(df, graph):
    selected_columns = {**LITERAL_CONCEPTS_COLUMNS,
                        **URI_CONCEPTS_COLUMNS}
    concept_maker = ConceptTripleMaker(df=df,
                                       column_mapping_dict=selected_columns,
                                       graph=graph,
                                       subject_in_scheme=LAM_CS,
                                       comment_predicate=SKOS.editorialNote,
                                       target_columns=[*selected_columns],
                                       literal_columns=[*LITERAL_CONCEPTS_COLUMNS],
                                       subject_source_column=URI_COLUMN,
                                       subject_classes=[SKOS.Concept, LAM.DocumentProperty])

    concept_maker.make_triples()

    in_collection_maker = InverseTripleMaker(df=df,
                                             column_mapping_dict=COLLECTION_COLUMNS,
                                             graph=graph,
                                             target_columns=[*COLLECTION_COLUMNS],
                                             subject_source_column=URI_COLUMN
                                             )

    in_collection_maker.make_triples()

    constraint_maker = ConstraintTripleMaker(df=df,
                                             column_mapping_dict=CONSTRAINT_COLUMNS,
                                             graph=graph,
                                             target_columns=[*CONSTRAINT_COLUMNS],
                                             constraint_property=LAM.hasAnnotationConfiguration,
                                             constraint_value_property=SHACL['class'],
                                             constraint_path_property=LAM.path,
                                             constraint_class=LAM.AnnotationConfiguration,
                                             constraint_comment=SKOS.editorialNote,
                                             subject_source_column=URI_COLUMN)
    constraint_maker.make_triples()


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


def make_property_worksheet(lam_df_properties, lam_df_property_classification, prefixes, output_file):
    """
    :param lam_df_property_classification:
    :param lam_df_properties:
    :param prefixes:
    :param output_file:
    :return:
    """
    graph = lam4vb3.lam_utils.make_graph(prefixes)
    create_concept_scheme(graph)
    create_concepts(lam_df_properties, graph)
    create_collections(lam_df_property_classification, graph)
    graph.serialize(str(output_file), format='turtle', )
    return graph
