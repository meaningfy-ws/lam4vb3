#!/usr/bin/python3

# property_builder.py
# Date:  05/08/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com

""" """
import rdflib
from rdflib import SKOS, RDF

import lam4vb3.lam_utils
from lam4vb3.builder import LAM, LAMD
from lam4vb3.builder.inverse_builders import InverseTripleMaker
from lam4vb3.builder.reified_builders import ConstraintTripleMaker
from lam4vb3.builder.simple_builders import ConceptTripleMaker, SimpleTripleMaker

LITERAL_CONCEPTS_COLUMNS = {
    'LABEL': 'skos:prefLabel@en',
    'KEYWORD': 'skos:altLabel@en',
    'EXAMPLE_EN': 'skos:example@en',
    'EXAMPLE_FR': 'skos:example@fr',
    'COMMENT': 'skos:editorialNote@en',
    'EXAMPLE_CELEX': 'skos:example',
}

MAPPING_PROPERTY_CONFIGURATION_COLUMNS = {
    'CDM_CLASS': 'lamd:md_CDM_CLASS',
    'DN_CLASS': 'lamd:md_DN_CLASS',
    'AU': 'lamd:md_AU',
    'FM': 'lamd:md_FM',
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

CONSTRAINT_COLUMNS = {
    'DT_CORR': 'lamd:md_DT_CORR',
    'DN': 'lamd:md_DN',
    'DC': 'lamd:md_DC',
    'CT': 'lamd:md_CT',
    'CC': 'lamd:md_CC',
    'RJ_NEW': 'lamd:md_RJ_NEW',
    'DD': 'lamd:md_DD',
    'IF': 'lamd:md_IF',
    'EV': 'lamd:md_EV',
    'NF': 'lamd:md_NF',
    'TP': 'lamd:md_TP',
    'SG': 'lamd:md_SG',
    'VO': 'lamd:md_VO',
    'DB': 'lamd:md_DB',
    'LO': 'lamd:md_LO',
    'DH': 'lamd:md_DH',
    'DL': 'lamd:md_DL',
    'RP': 'lamd:md_RP',
    'VV': 'lamd:md_VV',
    # 'REP': 'lamd:md_REP',
    'RS': 'lamd:md_RS',
    'AS': 'lamd:md_AS',
    'AF': 'lamd:md_AF',
    'MI': 'lamd:md_MI',
    'LG': 'lamd:md_LG',
    'RI': 'lamd:md_RI',
    'DP': 'lamd:md_DP',
    'AD': 'lamd:md_AD',
    'LF': 'lamd:md_LF',
    'REPPORTEUR': 'lamd:md_REPPORTEUR',
    'IC': 'lamd:md_IC',
    'CM': 'lamd:md_CM',
    'NS': 'lamd:md_NS',
    'TT': 'lamd:md_TT',
    'LB': 'lamd:md_LB',
    'AMENDMENT': 'lamd:md_AMENDMENT',
    'ADDITION': 'lamd:md_ADDITION',
    'REPEAL': 'lamd:md_REPEAL',
    'REPEAL_IMP': 'lamd:md_REPEAL_IMP',
    'ADOPTION': 'lamd:md_ADOPTION',
    'ADOPTION_PAR': 'lamd:md_ADOPTION_PAR',
    'APPLICABILITY_EXT': 'lamd:md_APPLICABILITY_EXT',
    'COMPLETION': 'lamd:md_COMPLETION',
    'VALIDITY_EXT': 'lamd:md_VALIDITY_EXT',
    'REPLACEMENT': 'lamd:md_REPLACEMENT',
    'CORRIGENDUM': 'lamd:md_CORRIGENDUM',
    'OBSOLETE': 'lamd:md_OBSOLETE',
    'DEROGATION': 'lamd:md_DEROGATION',
    'CONFIRMATION': 'lamd:md_CONFIRMATION',
    'QUESTION_SIMILAR': 'lamd:md_QUESTION_SIMILAR',
    'INTERPRETATION': 'lamd:md_INTERPRETATION',
    'IMPLEMENTATION': 'lamd:md_IMPLEMENTATION',
    'REESTAB': 'lamd:md_REESTAB',
    'SUSPEND': 'lamd:md_SUSPEND',
    'SUSPEND_PAR': 'lamd:md_SUSPEND_PAR',
    'APPLICABILITY_DEF': 'lamd:md_APPLICABILITY_DEF',
    'INCORPORATION': 'lamd:md_INCORPORATION',
    'REFER_PAR': 'lamd:md_REFER_PAR',
    'QUESTION_RELATED': 'lamd:md_QUESTION_RELATED',
    'OPINION_EP': 'lamd:md_OPINION_EP',
    'OPINION_COR': 'lamd:md_OPINION_COR',
    'OPINION_EESC': 'lamd:md_OPINION_EESC',
    'INFLUENCE': 'lamd:md_INFLUENCE',
    'AMENDMENT_PRO': 'lamd:md_AMENDMENT_PRO',
    'CI': 'lamd:md_CI',
    'RELATION': 'lamd:md_RELATION',
    'ASSOCIATION': 'lamd:md_ASSOCIATION',
    'PROC': 'lamd:md_PROC',
    'AP': 'lamd:md_AP',
    'DF': 'lamd:md_DF',
    'PR': 'lamd:md_PR',
    'NA': 'lamd:md_NA',
    'ANNULMENT_REQ': 'lamd:md_ANNULMENT_REQ',
    'FAILURE_REQ': 'lamd:md_FAILURE_REQ',
    'INAPPLICAB_REQ': 'lamd:md_INAPPLICAB_REQ',
    'ANULMENT_PARTIAL_REQ': 'lamd:md_ANULMENT_PARTIAL_REQ',
    'REVIEW_REQ': 'lamd:md_REVIEW_REQ',
    'PRELIMINARY_REQ': 'lamd:md_PRELIMINARY_REQ',
    'COMMUNIC_REQ': 'lamd:md_COMMUNIC_REQ',
    'OPINION_REQ': 'lamd:md_OPINION_REQ',
}

COLLECTION_COLUMNS = {"CLASSIFICATION": "skos:member"}

LAM_CS = LAMD.LAMClasses

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
                                       subject_classes=[SKOS.Concept, LAM.LegalDocumentClass])

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
                                             constraint_property=LAM.hasPropertyConfiguration,
                                             constraint_class=LAM.PropertyConfiguration,
                                             constraint_comment=SKOS.editorialNote,
                                             constraint_path_property=LAM.path,
                                             subject_source_column=URI_COLUMN)
    constraint_maker.make_triples()

    constraint_mapping_maker = ConstraintTripleMaker(df=df,
                                                     column_mapping_dict=MAPPING_PROPERTY_CONFIGURATION_COLUMNS,
                                                     graph=graph,
                                                     target_columns=[*MAPPING_PROPERTY_CONFIGURATION_COLUMNS],
                                                     constraint_property=LAM.classifyWith,
                                                     constraint_class=LAM.MappingPropertyConfiguration,
                                                     constraint_comment=SKOS.editorialNote,
                                                     constraint_path_property=LAM.path,
                                                     subject_source_column=URI_COLUMN)
    constraint_mapping_maker.make_triples()


def create_collections(df, graph):
    collection_maker = SimpleTripleMaker(df=df,
                                         column_mapping_dict=LITERAL_COLLECTIONS_COLUMNS,
                                         graph=graph,
                                         target_columns=[*LITERAL_COLLECTIONS_COLUMNS],
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


def make_lam_classes_worksheet(lam_df_classes, lam_df_classes_classification, prefixes, output_file):
    """
    :param lam_df_classes_classification:
    :param lam_df_classes:
    :param prefixes:
    :param output_file:
    :return:
    """
    graph = lam4vb3.lam_utils.make_graph(prefixes)
    create_concept_scheme(graph)
    create_concepts(lam_df_classes, graph)
    create_collections(lam_df_classes_classification, graph)
    graph.serialize(str(output_file), format='turtle', )
    return graph
