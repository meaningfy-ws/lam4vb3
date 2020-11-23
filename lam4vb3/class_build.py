"""
class_build
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import rdflib
from rdflib.namespace import RDF, SKOS, DCTERMS, OWL, XMLNS, XSD
from lam4vb3 import lam_utils, build, collection_build

SHACL = rdflib.Namespace("http://www.w3.org/ns/shacl#")
LAM = rdflib.Namespace("http://publications.europa.eu/ontology/lam-skos-ap#")

URI_COLUMN = 'URI'

LITERAL_COLUMNS = {
    'EXAMPLE_EN': 'skos:example@en',
    'EXAMPLE_FR': 'skos:example@fr',
    'COMMENT': 'skos:editorialNote@en',
    'EXAMPLE_CELEX': 'skos:example',
    'KEYWORD': 'skos:altLabel@en',
    'LABEL': 'skos:prefLabel@en',
}

MAPPING_VALUE_COMMENT_COLUMNS = {
    'CDM_CLASS': 'lamd:md_CDM_CLASS',
    'DN_CLASS': 'lamd:md_DN_CLASS',
    'AU': 'lamd:md_AU',
    'FM': 'lamd:md_FM',
}

CONSTRAINT_VALUE_COMMENT_COLUMNS = {
    # 'CODE': 'lamd:md_CODE',
    # 'LABEL': 'lamd:md_LABEL',
    # 'KEYWORD': 'lamd:md_KEYWORD',
    # 'EXAMPLE_EN': 'lamd:md_EXAMPLE_EN',
    # 'EXAMPLE_FR': 'lamd:md_EXAMPLE_FR',
    # 'COMMENT': 'lamd:md_COMMENT',
    # 'EXAMPLE_CELEX': 'lamd:md_EXAMPLE_CELEX',
    # 'CDM_CLASS': 'lamd:md_CDM_CLASS',
    # 'AU': 'lamd:md_AU',
    # 'FM': 'lamd:md_FM',
    # 'DN_CLASS': 'lamd:md_DN_CLASS',

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
    'REP': 'lamd:md_REP',
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

URI_CELEX_COLUMNS = {'PARENT': 'skos:broader', }

# COLLECTION_TARGET_COLUMNS = ["Classification level 1", "Classification level 2", "Classification level 3"]
#
# COLLECTION_COLUMNS = {
#     "Classification level 1": "skos:prefLabel",
#     "Classification level 2": "skos:prefLabel",
#     "Classification level 3": "skos:prefLabel",
# }


COLUMN_ANNOTATION_ASSOCIATIONS = [('DD', 'ANN_COD(DD)'), ('EV', 'ANN_COD(EV)'), ('SG', 'ANN_COD(SG)'), ]

ANNOTATION_COLUMNS = {
    'ANN_COD(DD)': 'lamd:md_ANN_COD',
    'ANN_COD(EV)': 'lamd:md_ANN_COD',
    'ANN_COD(SG)': 'lamd:md_ANN_COD',
    'DD': 'lamd:md_DD',
    'EV': 'lamd:md_EV',
    'SG': 'lamd:md_SG',
}

ANNOTATION_COLUMNS_UNUSED = {
    'ANN_COD': 'lamd:md_ANN_COD',
    'ANN_TOD': 'lamd:md_ANN_TOD',
    'ANN_CLB': 'lamd:md_ANN_CLB',
    'ANN_ART': 'lamd:md_ANN_ART',
    'ANN_PAR': 'lamd:md_ANN_PAR',
    'ANN_SUB': 'lamd:md_ANN_SUB',
    'ANN_TLT': 'lamd:md_ANN_TLT',
    'ANN_RL2': 'lamd:md_ANN_RL2',
    'ANN_MDL': 'lamd:md_ANN_MDL',
    'ANN_MSL': 'lamd:md_ANN_MSL',
    'ANN_SOV': 'lamd:md_ANN_SOV',
    'ANN_EOV': 'lamd:md_ANN_EOV',
    'ANN_LVL': 'lamd:md_ANN_LVL',
    'ANN_FCS': 'lamd:md_ANN_FCS',
    'ANN_FCT': 'lamd:md_ANN_FCT'}

LAM_CLASS_CS = "lamd:LAMLegalDocument"

CELEX_CS = "celexd:CelexLegalDocument"

LITERAL_CELEX_COLUMNS = {'CODE': 'skos:notation',
                         'LABEL': 'skos:prefLabel@en',
                         'EXAMPLE_EN': 'skos:example@en',
                         'COMMENT': 'skos:editorialNote@en',
                         }

VALUE_COMMENT_CELEX_COLUMNS = {
    'DTS': 'lam:dts',
    'DTT': 'lam:dtt',
    'DTA': 'lam:dta',
    'DTN': 'lam:dts',
}


def create_cs(graph, cs=LAM_CLASS_CS, cs_label="Document metadata"):
    """
        create the concept scheme definition
    """
    cs = lam_utils.qname_uri(cs, graph.namespaces())
    graph.add((cs, RDF.type, SKOS.ConceptScheme))
    graph.add((cs, SKOS.prefLabel, rdflib.Literal(cs_label)))


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
                                                                   uri_valued_columns=[],
                                                                   multi_line_columns=[],
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
                                                                       multi_line_columns=[],
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
    graph = build.make_graph(prefixes)
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
    graph = build.make_graph(prefixes)
    create_cs(graph, cs=CELEX_CS, cs_label="CELEX classes")
    create_celex_concepts(celex_df_classes, graph)

    collection_build.add_concept_to_collection(celex_df_classes, graph)
    collection_build.create_collections(celex_df_classes_classification, graph)

    graph.serialize(str(output_file), format='turtle', )
    return graph
