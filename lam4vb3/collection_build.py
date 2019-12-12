"""
collection_build.py
Date: 23/11/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""
from lam4vb3 import build

URI_COLUMN = 'URI'

LITERAL_COLUMNS = {
    'CODE': 'skos:notation',
    'LABEL': 'skos:prefLabel@en',
    'DESCRIPTION': 'skos:definition@en',
    'COMMENT': 'skos:editorialNote@en',
    'ORDER': 'euvoc:order',
}

COLLECTION_COLUMNS = {"CLASSIFICATION": "skos:member", }

URI_COLUMNS = {
    'PARENT': 'skos:member',
}


def create_collections(lam_df_property_classification, graph):
    """
    :return:
    """

    cm = build.ConceptTripleMaker(df=lam_df_property_classification,
                                  column_mapping_dict={**LITERAL_COLUMNS, **URI_COLUMNS},
                                  graph=graph,
                                  subject_in_scheme=None,
                                  target_columns=LITERAL_COLUMNS.keys(),
                                  uri_valued_columns=[],
                                  subject_source="URI",
                                  subject_class="skos:Collection",
                                  multi_line_columns=[], )
    cm.make_triples()

    im = build.InverseTripleMaker(df=lam_df_property_classification,
                                  column_mapping_dict=URI_COLUMNS,
                                  graph=graph,
                                  target_columns=URI_COLUMNS.keys(),
                                  subject_source="URI", )
    im.make_triples()


def add_concept_to_collection(df, graph):
    """
        add the concept to a collection as an inverse relation from the cell to the row subject.
    :param df:
    :param graph:
    :return:
    """
    im = build.InverseTripleMaker(df=df,
                                  column_mapping_dict=COLLECTION_COLUMNS,
                                  graph=graph,
                                  target_columns=COLLECTION_COLUMNS.keys(),
                                  subject_source="URI", )
    im.make_triples()
