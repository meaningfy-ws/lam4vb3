"""
class_build
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import rdflib
from rdflib.namespace import RDF, SKOS, DCTERMS, OWL, XMLNS, XSD

import lam4vb3.cell_parser
import lam4vb3.lam_utils
from lam4vb3 import lam_utils, build, collection_build

URI_COLUMN = 'URI'

LITERAL_COLUMNS = {
    'EXAMPLE_EN': 'skos:example@en',
    'EXAMPLE_FR': 'skos:example@fr',
    'COMMENT': 'skos:editorialNote@en',
    'EXAMPLE_CELEX': 'skos:example',
    'KEYWORD': 'skos:altLabel@en',
    'LABEL': 'skos:prefLabel@en',
    'DESCRIPTION': 'skos:description',
    'Analytical methodology': 'skos:scopeNote@en',
    'Specific cases': 'skos:historyNote@en',
    'CODE': 'skos:notation'
}

MAPPING_VALUE_COMMENT_COLUMNS = {
    'CDM_CLASS': 'lamd:md_CDM_CLASS',
    'DN_CLASS': 'lamd:md_DN_CLASS',
    'AU': 'lamd:md_AU',
    'FM': 'lamd:md_FM',
}

CONSTRAINT_VALUE_COMMENT_COLUMNS = {
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
    "AD": "lamd:md_AD",
    "ADDITION": "lamd:md_ADDITION",
    "ADOPTION": "lamd:md_ADOPTION",
    "ADOPTION_PAR": "lamd:md_ADOPTION_PAR",
    "AF": "lamd:md_AF",
    "AMENDMENT": "lamd:md_AMENDMENT",
    "AMENDMENT_PRO": "lamd:md_AMENDMENT_PRO",
    "ANNULMENT_REQ": "lamd:md_ANNULMENT_REQ",
    "ANULMENT_PARTIAL_REQ": "lamd:md_ANULMENT_PARTIAL_REQ",
    "AP": "lamd:md_AP",
    "APPLICABILITY_DEF": "lamd:md_APPLICABILITY_DEF",
    "APPLICABILITY_EXT": "lamd:md_APPLICABILITY_EXT",
    "AS": "lamd:md_AS",
    "ASSOCIATION": "lamd:md_ASSOCIATION",
    "CC": "lamd:md_CC",
    "CI": "lamd:md_CI",
    "CM": "lamd:md_CM",
    "COMMUNIC_REQ": "lamd:md_COMMUNIC_REQ",
    "COMPLETION": "lamd:md_COMPLETION",
    "CONFIRMATION": "lamd:md_CONFIRMATION",
    "CORRIGENDUM": "lamd:md_CORRIGENDUM",
    "CT": "lamd:md_CT",
    "DB": "lamd:md_DB",
    "DD": "lamd:md_DD",
    "DEROGATION": "lamd:md_DEROGATION",
    "DF": "lamd:md_DF",
    "DH": "lamd:md_DH",
    "DL": "lamd:md_DL",
    "DP": "lamd:md_DP",
    "DR": "lamd:md_DR",
    "ECLI": "lamd:md_ECLI",
    "ELI": "lamd:md_ELI",
    "EV": "lamd:md_EV",
    "FAILURE_REQ": "lamd:md_FAILURE_REQ",
    "IC": "lamd:md_IC",
    "IF": "lamd:md_IF",
    "IMPLEMENTATION": "lamd:md_IMPLEMENTATION",
    "INAPPLICAB_REQ": "lamd:md_INAPPLICAB_REQ",
    "INCORPORATION": "lamd:md_INCORPORATION",
    "INFLUENCE": "lamd:md_INFLUENCE",
    "INTERPRETATION": "lamd:md_INTERPRETATION",
    "LB": "lamd:md_LB",
    "LF": "lamd:md_LF",
    "LG": "lamd:md_LG",
    "LO": "lamd:md_LO",
    "MI": "lamd:md_MI",
    "NA": "lamd:md_NA",
    "NF": "lamd:md_NF",
    "NS": "lamd:md_NS",
    "OBSOLETE": "lamd:md_OBSOLETE",
    "OPINION_COR": "lamd:md_OPINION_COR",
    "OPINION_EESC": "lamd:md_OPINION_EESC",
    "OPINION_EP": "lamd:md_OPINION_EP",
    "OPINION_REQ": "lamd:md_OPINION_REQ",
    "PR": "lamd:md_PR",
    "PRELIMINARY_REQ": "lamd:md_PRELIMINARY_REQ",
    "PROC": "lamd:md_PROC",
    "QUESTION_RELATED": "lamd:md_QUESTION_RELATED",
    "QUESTION_SIMILAR": "lamd:md_QUESTION_SIMILAR",
    "REESTAB": "lamd:md_REESTAB",
    "REFER_PAR": "lamd:md_REFER_PAR",
    "RELATION": "lamd:md_RELATION",
    "REP": "lamd:md_REP",
    "REPEAL": "lamd:md_REPEAL",
    "REPEAL_IMP": "lamd:md_REPEAL_IMP",
    "REPLACEMENT": "lamd:md_REPLACEMENT",
    "REPPORTEUR": "lamd:md_REPPORTEUR",
    "REVIEW_REQ": "lamd:md_REVIEW_REQ",
    "RI": "lamd:md_RI",
    "RI_WORK": "lamd:md_RI_WORK",
    "RJ_NEW": "lamd:md_RJ_NEW",
    "RP": "lamd:md_RP",
    "RS": "lamd:md_RS",
    "SG": "lamd:md_SG",
    "SUSPEND": "lamd:md_SUSPEND",
    "SUSPEND_PAR": "lamd:md_SUSPEND_PAR",
    "TOF": "lamd:md_TOF",
    "TP": "lamd:md_TP",
    "TT": "lamd:md_TT",
    "VALIDITY_EXT": "lamd:md_VALIDITY_EXT",
    "VO": "lamd:md_VO",
    "VV": "lamd:md_VV",

    'DT_CORR': 'lamd:md_DT_CORR',
    'DN': 'lamd:md_DN',
    'DC': 'lamd:md_DC',

}



URI_CELEX_COLUMNS = {'PARENT': 'skos:broader', }



LAM_CLASS_CS = "lamd:LAMLegalDocument"

CELEX_CS = "celexd:CelexLegalDocument"

LAM_PROPRITIES = "lam:DocumentProperty"







def create_concepts(df, graph):
    """
        create the concepts
    :param df:
    :param graph:
    :return:
    """
    # make literal columns
    literal_maker = build.ConceptTripleMaker(df,
                                             subject_source=URI_COLUMN,
                                             subject_class="skos:Concept",
                                             subject_in_scheme=LAM_CLASS_CS,
                                             column_mapping_dict=LITERAL_COLUMNS,
                                             target_columns=list(LITERAL_COLUMNS.keys()),
                                             uri_valued_columns=[],
                                             multi_line_columns=[],
                                             graph=graph)
    literal_maker.make_triples()

    # # make uri columns
    # uri_maker = build.ConceptTripleMaker(df,
    #                                      subject_source=URI_COLUMN,
    #                                      subject_class="skos:Concept",
    #                                      subject_in_scheme=LAM_CLASS_CS,
    #                                      column_mapping_dict=MAPPING_URI_COLUMNS,
    #                                      target_columns=list(MAPPING_URI_COLUMNS.keys()),
    #                                      uri_valued_columns=list(MAPPING_URI_COLUMNS.keys()),
    #                                      multi_line_columns=[],
    #                                      graph=graph)
    #
    # uri_maker.make_triples()

    # make constraint from value with comment: Author
    value_comment_constraint_maker = build.ConceptConstraintMaker(df,
                                                                  subject_source=URI_COLUMN,
                                                                  subject_class="skos:Concept",
                                                                  subject_in_scheme=LAM_CLASS_CS,
                                                                  constraint_property="lam:classifyWith",
                                                                  constraint_class="lam:MappingPropertyConfiguration",
                                                                  constraint_comment="skos:editorialNote",
                                                                  constraint_path_property="lam:path",
                                                                  column_mapping_dict=MAPPING_VALUE_COMMENT_COLUMNS,
                                                                  target_columns=list(
                                                                      MAPPING_VALUE_COMMENT_COLUMNS.keys()),
                                                                  uri_valued_columns=list(
                                                                      MAPPING_VALUE_COMMENT_COLUMNS.keys()),
                                                                  multi_line_columns=list(
                                                                      MAPPING_VALUE_COMMENT_COLUMNS.keys()),
                                                                  graph=graph)

    value_comment_constraint_maker.make_triples()

    # # make constraint from value with comment: Mapping columns
    # value_comment_constraint_maker1 = build.ConceptConstraintMaker(df,
    #                                                                subject_source=URI_COLUMN,
    #                                                                subject_class="skos:Concept",
    #                                                                subject_in_scheme=LAM_CLASS_CS,
    #                                                                constraint_property="lam:hasPropertyConfiguration",
    #                                                                constraint_class="lam:MappingPropertyConfiguration",
    #                                                                constraint_comment="skos:editorialNote",
    #                                                                column_mapping_dict=MAPPING_URI_COLUMNS,
    #                                                                target_columns=list(MAPPING_URI_COLUMNS.keys()),
    #                                                                uri_valued_columns=list(MAPPING_URI_COLUMNS.keys()),
    #                                                                multi_line_columns=[],
    #                                                                graph=graph)
    #
    # value_comment_constraint_maker1.make_triples()

    # make constraint from values with comments (according to agreed cardinality specs)
    value_comment_constraint_maker3 = build.ConceptConstraintMaker(df,
                                                                   subject_source=URI_COLUMN,
                                                                   subject_class="skos:Concept",
                                                                   subject_in_scheme=LAM_CLASS_CS,
                                                                   constraint_property="lam:hasPropertyConfiguration",
                                                                   constraint_class="lam:PropertyConfiguration",
                                                                   constraint_comment="skos:editorialNote",
                                                                   constraint_path_property="lam:path",
                                                                   column_mapping_dict=CONSTRAINT_VALUE_COMMENT_COLUMNS,
                                                                   target_columns=list(
                                                                       CONSTRAINT_VALUE_COMMENT_COLUMNS.keys()),
                                                                   uri_valued_columns=CONSTRAINT_VALUE_URI_COLUMN_LIST,
                                                                   multi_line_columns=CONSTRAINT_VALUE_MULTI_LINE_COLUMNS_LIST,
                                                                   graph=graph)

    value_comment_constraint_maker3.make_triples()

    # add annotation constraint statements afferent to property constrain on the Document classes
    for concept_property_column, property_annotation_column in COLUMN_ANNOTATION_ASSOCIATIONS:
        # make constraint from value with comment: Cardinality specs on concept property constraints with annotations
        value_comment_constraint_maker5 = build.ConceptConstraintMaker(df,
                                                                       subject_source=[concept_property_column],
                                                                       subject_class="lam:PropertyConfiguration",
                                                                       subject_in_scheme=None,
                                                                       constraint_property="lam:hasAnnotationConfiguration",
                                                                       constraint_class="lam:AnnotationConfiguration",
                                                                       constraint_path_property="lam:path",
                                                                       column_mapping_dict=ANNOTATION_COLUMNS,
                                                                       target_columns=[property_annotation_column],
                                                                       uri_valued_columns=[property_annotation_column],
                                                                       multi_line_columns=list(
                                                                           ANNOTATION_COLUMNS.keys()),
                                                                       # originally the anotation colums were not treated as multi-line
                                                                       graph=graph)

        value_comment_constraint_maker5.make_triples()


# def create_collections(df, graph):
#     """
#
#     :param df:
#     :param graph:
#     :return:
#     """
#     collection_maker = build.ConceptCollectionMaker(df,
#                                                     column_mapping_dict=COLLECTION_COLUMNS,
#                                                     graph=graph,
#                                                     target_columns=COLLECTION_TARGET_COLUMNS,
#                                                     subject_source="URI",
#                                                     subject_class="skos:Concept",
#                                                     membership_predicate="skos:member",
#                                                     collection_class="skos:Collection", )
#     collection_maker.make_triples()


def create_celex_concepts(df, graph):
    """

    :param df:
    :param graph:
    :return:
    """
    # make literal columns
    literal_maker = build.ConceptTripleMaker(df,
                                             subject_source=URI_COLUMN,
                                             subject_class="skos:Concept",
                                             subject_in_scheme=CELEX_CS,
                                             column_mapping_dict=LITERAL_CELEX_COLUMNS,
                                             target_columns=list(LITERAL_CELEX_COLUMNS.keys()),
                                             uri_valued_columns=[],
                                             multi_line_columns=[],
                                             graph=graph)
    literal_maker.make_triples()

    # # make uri columns
    uri_maker = build.ConceptTripleMaker(df,
                                         subject_source=URI_COLUMN,
                                         subject_class="skos:Concept",
                                         subject_in_scheme=CELEX_CS,
                                         column_mapping_dict=URI_CELEX_COLUMNS,
                                         target_columns=list(URI_CELEX_COLUMNS.keys()),
                                         uri_valued_columns=list(URI_CELEX_COLUMNS.keys()),
                                         multi_line_columns=[],
                                         graph=graph)

    uri_maker.make_triples()

    # make constraint from values with comments (according to agreed cardinality specs)
    value_comment_constraint_maker = build.ConceptConstraintMaker(df,
                                                                  subject_source=URI_COLUMN,
                                                                  subject_class="skos:Concept",
                                                                  subject_in_scheme=CELEX_CS,
                                                                  constraint_property="lam:hasPropertyConfiguration",
                                                                  constraint_class="lam:PropertyConfiguration",
                                                                  constraint_comment="skos:editorialNote",
                                                                  constraint_path_property="lam:path",
                                                                  column_mapping_dict=VALUE_COMMENT_CELEX_COLUMNS,
                                                                  target_columns=list(
                                                                      VALUE_COMMENT_CELEX_COLUMNS.keys()),
                                                                  uri_valued_columns=[],
                                                                  multi_line_columns=[],
                                                                  graph=graph)

    value_comment_constraint_maker.make_triples()


def make_class_worksheet(lam_df_classes, lam_df_class_classification, prefixes, output_file):
    """
    :param lam_df_class_classification:
    :param lam_df_classes:
    :param prefixes:
    :param output_file:
    :return:
    """
    graph = lam4vb3.lam_utils.make_graph(prefixes)
    create_cs(graph, cs=LAM_CLASS_CS, cs_label="LAM classes")
    # create_collections(lam_df_classes, graph)
    collection_build.create_collections(lam_df_class_classification, graph)
    collection_build.add_concept_to_collection(lam_df_classes, graph)

    create_concepts(lam_df_classes, graph)
    graph.serialize(str(output_file), format='turtle', )
    return graph


def make_celex_class_worksheet(celex_df_classes, celex_df_classes_classification, prefixes, output_file):
    """

    :param celex_df_classes_classification:
    :param celex_df_classes:
    :param prefixes:
    :param output_file:
    :return:
    """
    # ugly column type correction, TODO: make more elegant and generic
    celex_df_classes['DTS'] = celex_df_classes['DTS'].apply(str)
    celex_df_classes['CODE'] = celex_df_classes['CODE'].apply(str)

    # ugly column type correction, TODO: make more elegant and generic
    celex_df_classes['DTS'] = celex_df_classes['DTS'].apply(str)
    celex_df_classes_classification['CODE'] = celex_df_classes_classification['CODE'].apply(str)
    #
    graph = lam4vb3.lam_utils.make_graph(prefixes)
    create_cs(graph, cs=CELEX_CS, cs_label="CELEX classes")
    create_celex_concepts(celex_df_classes, graph)

    collection_build.create_collections(celex_df_classes_classification, graph)
    collection_build.add_concept_to_collection(celex_df_classes, graph)

    graph.serialize(str(output_file), format='turtle', )
    return graph
