#!/usr/bin/python3

# test_concept_triple_maker.py
# Date:  05/08/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import rdflib
from rdflib import SKOS, RDFS, RDF

from lam4vb3.builder import LAMD, SHACL, CDM
from lam4vb3.builder.simple_builders import ConceptTripleMaker, SimpleTripleMaker
from lam4vb3.lam_utils import generate_uuid_uri

TEST_LITERAL_COLUMNS_PROPERTY_DF = {
    'CODE': 'skos:notation',
    'LABEL': 'skos:prefLabel@en',
    'DESCRIPTION': 'skos:definition@en',
    'Example - cellar notice': 'skos:example',
    'Analytical methodology': 'skos:scopeNote@en',
    'Specific cases': 'skos:historyNote@en',
    'Comments': 'skos:editorialNote@en',
    'Changes to be done': 'skos:editorialNote@en',
    'PROP_TYPE': 'dct:type',
}

TEST_URI_COLUMNS_PROPERTY_DF = {
    'SH_PATH': 'sh:path',
}

TEST_LITERAL_COLUMNS_CLASSIFICATION = {
    'CODE': 'skos:notation',
    'LABEL': 'skos:prefLabel@en',
    'DESCRIPTION': 'skos:definition@en',
    'COMMENT': 'skos:editorialNote@en',
    'ORDER': 'euvoc:order',
}

TEST_URI_COLUMNS_CLASSIFICATION = {
    'PARENT_COLLECTION': 'skos:member',
}

URI_COLUMN = 'URI'


def test_in_scheme(test_lam_properties_df, empty_lam_graph):
    selected_cols = {**TEST_LITERAL_COLUMNS_PROPERTY_DF,
                     **TEST_URI_COLUMNS_PROPERTY_DF
                     }

    TEST_CONCEPT_SCHEME = generate_uuid_uri("123", empty_lam_graph)

    c = ConceptTripleMaker(df=test_lam_properties_df,
                           column_mapping_dict=selected_cols,
                           graph=empty_lam_graph,
                           subject_in_scheme=TEST_CONCEPT_SCHEME,
                           comment_predicate=SKOS.editorialNote,
                           target_columns=[*selected_cols],
                           literal_columns=[*TEST_LITERAL_COLUMNS_PROPERTY_DF],
                           subject_source_column="URI",
                           subject_classes=[SKOS.Concept, RDFS.Resource], )
    c.make_triples()

    # assert empty_lam_graph.query("ASK {?s skos:inScheme ?cs}")
    assert (None, SKOS.inScheme, TEST_CONCEPT_SCHEME) in empty_lam_graph
    assert (LAMD.md_AU, SKOS.prefLabel, rdflib.Literal(lexical_or_value="Author", lang="en")) in empty_lam_graph
    assert (LAMD.md_AU, SHACL.path, CDM.created_by) in empty_lam_graph
    assert (None, RDF.type, SKOS.Concept) in empty_lam_graph
    assert (None, RDF.type, RDFS.Resource) in empty_lam_graph
    # assert empty_lam_graph.query("ASK {?s skos:inScheme " + TEST_CONCEPT_SCHEME + "}")


def test_collection(test_lam_properties_classification_df, empty_lam_graph):
    selected_cols = {**TEST_LITERAL_COLUMNS_CLASSIFICATION,
                     **TEST_URI_COLUMNS_CLASSIFICATION
                     }

    collections = SimpleTripleMaker(df=test_lam_properties_classification_df,
                                    column_mapping_dict=selected_cols,
                                    graph=empty_lam_graph,
                                    target_columns=[*selected_cols],
                                    literal_columns=[*TEST_LITERAL_COLUMNS_CLASSIFICATION],
                                    subject_source_column=URI_COLUMN,
                                    subject_classes=[SKOS.Collection],
                                    comment_predicate=SKOS.editorialNote)
    collections.make_triples()

    assert (None, RDF.type, SKOS.Collection) in empty_lam_graph
    assert (LAMD.class_CLX, SKOS.prefLabel,
            rdflib.Literal(lexical_or_value="Celex number", lang="en")) in empty_lam_graph
    assert (LAMD.class_CLX, SKOS.member, LAMD.class_REF)

