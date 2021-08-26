from rdflib import SKOS

from lam4vb3.builder import LAMD
from lam4vb3.builder.inverse_builders import InverseTripleMaker

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


def test_classification(test_lam_properties_df, empty_lam_graph):
    colllections = InverseTripleMaker(df=test_lam_properties_df,
                                      column_mapping_dict=COLLECTION_COLUMNS,
                                      graph=empty_lam_graph,
                                      target_columns=[*COLLECTION_COLUMNS],
                                      subject_source_column=URI_COLUMN
                                      )

    colllections.make_triples()

    assert (LAMD.class_EDIT, SKOS.member, LAMD.md_KEYWORD) in empty_lam_graph
    assert (LAMD.class_EDIT, SKOS.member, LAMD.md_EXAMPLE_EN) in empty_lam_graph


