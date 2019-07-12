"""
class_build
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import pandas as pd
import rdflib
from rdflib import XSD, RDF, RDFS

from lam4vb3 import build, lam_utils

SHACL = rdflib.Namespace("http://www.w3.org/ns/shacl#")
LAM = rdflib.Namespace("http://publications.europa.eu/ontology/lam-skos-ap#")

URI_COLUMN = 'URI'

LITERAL_COLUMNS = {
    'EXAMPLE_EN': 'skos:example@en',
    'EXAMPLE_FR': 'skos:example@fr',
    'COMMENT': 'skos:editorialNote@en',
    'EXAMPLE_CELEX': 'skos:example',
}

REIFIED_LITERAL_COLUMNS = {
    'KEYWORD': 'skosxl:literalForm@en',
}

MAPPING_URI_COLUMNS = {
    'CDM_CLASS': 'lam:cdm_class',
    'DN_CLASS': 'lam:celex_class',
}

MAPPING_VALUE_COMMENT_COLUMNS = {
    'AU': 'cdm:created_by',
    'FM': 'cdm:resource-type',
}

CONSTRAINT_VALUE_COMMENT_COLUMNS = {
    'DN': 'cdm:resource_legal_id_celex',
    'DT_CORR': 'cdm:resource_legal_number_corrigendum',
    'DC': 'cdm:concept_eurovoc',
    'CT': 'cdm:resource_legal_is_about_subject-matter',
    'CC': 'cdm:resource_legal_is_about_concept_directory-code',
    'RJ_NEW': 'cdm:case-law_is_about_concept_new_case-law',
    'DD': 'cdm:work_date_document',
    'IF': 'cdm:resource_legal_date_entry-into-force',
    'EV': 'cdm:resource_legal_date_end-of-validity',
    'NF': 'cdm:legislation_secondary_date_notification',
    'TP': 'cdm:date_transposition',
    'SG': 'cdm:resource_legal_date_signature',
    'VO': 'cdm:resource_legal_date_vote',
    'DB': 'cdm:act_preparatory_date_debate',
    'LO': 'cdm:resource_legal_date_request_opinion',
    'DH': 'cdm:resource_legal_date_dispatch',
    'DL': 'cdm:resource_legal_date_deadline',
    'RP': 'cdm:question_parliamentary_date_reply',
    'VV': 'cdm:resource_legal_in-force',
    'REP': 'cdm:resource_legal_repertoire',
    'RS': 'cdm:service_responsible',
    'AS': 'cdm:service_associated',
    'AF': 'cdm:question_parliamentary_asked_by_group_parliamentary ',
    'MI': 'cdm:resource_legal_information_miscellaneous',
    'LG': 'cdm:term_parliamentary ',
    'RI': 'cdm:resource_legal_position_eesc',
    'DP': 'cdm:stored_by ',
    'AD': 'cdm:addresses',
    'LF': 'cdm:resource_legal_uses_originally_language',
    'NA': 'cdm:work_originates_in_country',
    'REPPORTEUR': 'cdm:reported_by',
    'IC': 'cdm:agreement_international_has_type_comment_concept_type_comment',
    'CM': 'cdm:resource_legal_comment_internal',
    'NS': 'cdm:preparatory_act_number_session',
    'TT': 'cdm:resource_legal_based_on_concept_treaty',
    'LB': 'cdm:resource_legal_based_on_resource_legal',
    'AMENDMENT': 'cdm:resource_legal_amends_resource_legal',
    'ADDITION': 'cdm:resource_legal_adds_to_resource_legal',
    'REPEAL': 'cdm:resource_legal_repeals_resource_legal',
    'REPEAL_IMP': 'cdm:resource_legal_implicitly_repeals_resource_legal',
    'ADOPTION': 'cdm:resource_legal_adopts_resource_legal',
    'ADOPTION_PAR': 'cdm:resource_legal_partially_adopts_resource_',
    'APPLICABILITY_EXT': 'cdm:resource_legal_extends_application_resource_legal',
    'COMPLETION': 'cdm:resource_legal_completes_resource_legal',
    'VALIDITY_EXT': 'cdm:resource_legal_extends_validity_of_resource_legal',
    'REPLACEMENT': 'cdm:resource_legal_replaces_resource_legal',
    'CORRIGENDUM': 'cdm:resource_legal_corrects_resource_legal',
    'OBSOLETE': 'cdm:resource_legal_renders_obsolete_resource_legal',
    'DEROGATION': 'cdm:resource_legal_derogates_resource_legal',
    'CONFIRMATION': 'cdm:resource_legal_confirms_resource_legal',
    'QUESTION_SIMILAR': 'cdm:resource_legal_tackles_similar_question_as_resource_legal',
    'INTERPRETATION': 'cdm:resource_legal_interpretes_authoritatively_resource_legal',
    'IMPLEMENTATION': 'cdm:resource_legal_implements_resource_legal',
    'REESTAB': 'cdm:resource_legal_reestablishes_resource_legal',
    'SUSPEND': 'cdm:resource_legal_suspends_resource_legal',
    'SUSPEND_PAR': 'cdm:resource_legal_partially_suspends_resource_legal',
    'APPLICABILITY_DEF': 'cdm:resource_legal_defers_application_of_resource_legal',
    'INCORPORATION': 'cdm:resource_legal_incorporates_resource_legal',
    'REFER_PAR': 'cdm:resource_legal_partially_refers_to_resource_legal',
    'QUESTION_RELATED': 'cdm:resource_legal_related_question_to_resource_legal',
    'OPINION_EP': 'cdm:resource_resource_legal_contains_ep_opinion_on_resource_legal',
    'OPINION_COR': 'cdm:resource_resource_legal_contains_cor_opinion_on_resource_legal',
    'OPINION_EESC': 'cdm:resource_resource_legal_contains_eesc_opinion_on_resource_legal',
    'INFLUENCE': 'cdm:resource_resource_legal_influences_resource_legal',
    'AMENDMENT_PRO': 'cdm:resource_resource_legal_proposes_to_amend_resource_legal',
    'CI': 'cdm:work_cites_work',
    'RELATION': 'cdm:work_related_to_work',
    'ASSOCIATION': 'cdm:resource_legal_associates_agreement_international',
    'PROC': 'cdm:work_part_of_dossier',
    'AP': 'cdm:communication_cjeu_requested_by_agent',
    'DF': 'cdm:communication_cjeu_defended_by_agent',
    'PR': 'cdm:communication_cjeu_has_type_procedure_concept_type_procedure',
    'ANNULMENT_REQ': 'cdm:communication_case_new_requests_annulment_of_resource_legal',
    'FAILURE_REQ': 'cdm:communication_case_new_requests_establishment_of_failure_of_obligation_resource_legal',
    'INAPPLICAB_REQ': 'cdm:communication_case_new_requests_inapplicability_resource_legal',
    'ANULMENT_PARTIAL_REQ': 'cdm:communication_case_new_requests_partial_annulment_of_resource_legal',
    'REVIEW_REQ': 'cdm:communication_case_new_requests_review_of_decision_case-law',
    'PRELIMINARY_REQ': 'cdm:communication_case_new_submits_preliminary_question_resource_legal',
    'COMMUNIC_REQ': 'cdm:communication_cjeu_communicates_on_case-law',
    'OPINION_REQ': 'cdm:communication_request_opinion_requests_opinion_on_resource_legal',
}

COLLECTION_COLUMNS = ["Classification level 1", "Classification level 2", "Classification level 3"]

COLUMN_ANNOTATION_ASSOCIATIONS = [('DD', 'ANN_COD(DD)'), ('EV', 'ANN_COD(EV)'), ('SG', 'ANN_COD(SG)'), ]

ANNOTATION_COLUMNS = {
    'ANN_COD(DD)': 'ann:comment_on_date',
    'ANN_COD(EV)': 'ann:comment_on_date',
    'ANN_COD(SG)': 'ann:comment_on_date',
    'DD': 'cdm:work_date_document',
    'EV': 'cdm:resource_legal_date_end-of-validity',
    'SG': 'cdm:resource_legal_date_signature',
}


class LAMConstraintTripleMaker(build.MultiColumnTripleMaker):

    def handle_object(self, row_index, target_column, language=None, data_type=None):

        cell_value = self.df.loc[row_index, target_column]
        graph = self.graph if target_column in self.uri_valued_columns else None

        if cell_value and pd.notna(cell_value):
            if target_column in self.multi_line_columns:
                objects = build.parse_multi_line_commented_value(cell_value,
                                                                 graph=graph,
                                                                 language=language,
                                                                 data_type=data_type, )
                return [x for x in objects if x]

            return [build.parse_commented_value(cell_value,
                                                graph=graph,
                                                language=language,
                                                data_type=data_type, )]

    def handle_cell_subject(self, value):
        """
            generate a repeatable cell specific uuid
        :type value: object
        :return: an UUID URI
        """

        return lam_utils.generate_uuid_uri(str(value),
                                           seed=str(self.df.head()),
                                           graph=self.graph,
                                           prefix="res_")

    def make_cell_triples(self, subject, predicate, oobject,):

        cell_subject = self.handle_cell_subject(row_index=str(subject) + str(predicate) + str(oobject))
        # TODO

        result_triples = [tuple([cell_subject, RDF.type, LAM.PropertyConstraint]),
                          tuple([cell_subject, SHACL.path, predicate]), ]
        for obj_value, obj_comment in oobject:
            if str(obj_value).strip().lower() is "y":
                result_triples.extend([
                    tuple([cell_subject, SHACL.name, rdflib.Literal(f"Mandatory {predicate}")]),
                    tuple([cell_subject, SHACL.minCount, rdflib.Literal("1", datatype=XSD.int)]),
                ])
            elif str(obj_value).strip().lower() is "yu":
                result_triples.extend([
                    tuple([cell_subject, SHACL.name, rdflib.Literal(f"Mandatory unique {predicate}")]),
                    tuple([cell_subject, SHACL.minCount, rdflib.Literal("1", datatype=XSD.int)]),
                    tuple([cell_subject, SHACL.maxCount, rdflib.Literal("1", datatype=XSD.int)]),
                ])
            elif str(obj_value).strip().lower() is "o":
                result_triples.extend([
                    tuple([cell_subject, SHACL.name, rdflib.Literal(f"Optional {predicate}")]),
                ])
            elif str(obj_value).strip().lower() is "ou":
                result_triples.extend([
                    tuple([cell_subject, SHACL.name, rdflib.Literal(f"Optional unique {predicate}")]),
                    tuple([cell_subject, SHACL.maxCount, rdflib.Literal("1", datatype=XSD.int)]),
                ])
            elif str(obj_value).strip().lower() is "n":
                result_triples.extend([
                    tuple([cell_subject, SHACL.name, rdflib.Literal(f"Forbidden {predicate}")]),
                    tuple([cell_subject, SHACL.maxCount, rdflib.Literal("0", datatype=XSD.int)]),
                ])
            else:
                result_triples.extend([
                    tuple([cell_subject, SHACL.maxCount, rdflib.Literal("0", datatype=XSD.int)]),
                ])
            if obj_comment:
                result_triples.append(tuple([cell_subject, RDFS.comment, rdflib.Literal(obj_comment)]))
        return result_triples
