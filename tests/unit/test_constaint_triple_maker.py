import rdflib
from rdflib import SH, DCTERMS, SKOS

from lam4vb3.builder import LAM, AT, LAMD, FD_365
from lam4vb3.builder.reified_builders import ConstraintTripleMaker, AnnotationConstraintTripleMaker
from tests.unit.conftest import TEMP_OUTPUT_FOLDER

URI_COLUMN = 'URI'

CONSTRAINT_COLUMNS = {
    "ANN_COD": "lamd:md_ANN_COD",
    "ANN_TOD": "lamd:md_ANN_TOD",
    "ANN_ART": "lamd:md_ANN_ART",
}

COLUMN_ANNOTATION_ASSOCIATIONS = {'ANN_COD(DD)': 'DD',
                                  'ANN_COD(DH)': 'DH',
                                  'ANN_COD(DL)': 'DL',
                                  'ANN_COD(EV)': 'EV',
                                  'ANN_COD(SG)': 'SG',
                                  'ANN_TOD(IF)': 'IF',
                                  'ANN_COD(IF)': 'IF'}

ANNOTATION_COLUMNS = {
    'ANN_COD(DD)': 'lamd:md_ANN_COD',
    'ANN_COD(DH)': 'lamd:md_ANN_COD',
    'ANN_COD(DL)': 'lamd:md_ANN_COD',
    'ANN_COD(EV)': 'lamd:md_ANN_COD',
    'ANN_COD(SG)': 'lamd:md_ANN_COD',
    'ANN_TOD(IF)': 'lamd:md_ANN_TOD',
    'ANN_COD(IF)': 'lamd:md_ANN_COD',
}

CONSTRAINT_LAM_CLASSES_COLUMNS = {
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
    'VV': 'lamd:md_VV'}


def test_constraint(test_lam_properties_df, empty_lam_graph):
    constraints = ConstraintTripleMaker(df=test_lam_properties_df,
                                        graph=empty_lam_graph,
                                        subject_source_column=URI_COLUMN,
                                        target_columns=[*CONSTRAINT_COLUMNS],
                                        column_mapping_dict=CONSTRAINT_COLUMNS,
                                        constraint_class=LAM.AnnotationConfiguration,
                                        constraint_property=LAM.hasAnnotationConfiguration,
                                        constraint_path_property=LAM.path
                                        )

    constraints.make_triples()

    empty_lam_graph.serialize(destination=TEMP_OUTPUT_FOLDER / "tbl.ttl")

    assert (LAM.md_CODE, LAM.hasAnnotationConfiguration, None) not in empty_lam_graph
    assert (LAMD.md_IF, LAM.hasAnnotationConfiguration, None) in empty_lam_graph
    assert (None, SH.hasValue, AT.fd_335) in empty_lam_graph


def test_annotated_constraint(test_lam_classes_df, empty_lam_graph):
    annotation_constraints_maker = AnnotationConstraintTripleMaker(df=test_lam_classes_df,
                                                                   graph=empty_lam_graph,
                                                                   constraint_property=LAM.hasAnnotationConfiguration,
                                                                   column_mapping_dict=ANNOTATION_COLUMNS,
                                                                   constraint_class=LAM.AnnotationConfiguration,
                                                                   target_columns=[*ANNOTATION_COLUMNS],
                                                                   annotation_column_mapping=COLUMN_ANNOTATION_ASSOCIATIONS,
                                                                   constraint_path_property=LAM.path
                                                                   )
    annotation_constraints_maker.make_triples()

    empty_lam_graph.serialize(destination=TEMP_OUTPUT_FOLDER / "annotations.ttl")

    assert (None, SH.hasValue, FD_365.DATSIG) in empty_lam_graph
    assert (None, SH.name, None) in empty_lam_graph
    assert (None, LAM.hasAnnotationConfiguration, None) in empty_lam_graph
    assert (None, LAM.path, LAMD.md_ANN_COD) in empty_lam_graph
    assert (None, SH.minCount, None) in empty_lam_graph
    assert (None, DCTERMS.created, None) in empty_lam_graph


def test_constraint_lam_classes(test_lam_classes_df, empty_lam_graph):
    constraints = ConstraintTripleMaker(df=test_lam_classes_df,
                                        graph=empty_lam_graph,
                                        subject_source_column=URI_COLUMN,
                                        target_columns=[*CONSTRAINT_LAM_CLASSES_COLUMNS],
                                        column_mapping_dict=CONSTRAINT_LAM_CLASSES_COLUMNS,
                                        constraint_class=LAM.PropertyConfiguration,
                                        constraint_property=LAM.hasPropertyConfiguration,
                                        constraint_comment=SKOS.editorialNote,
                                        constraint_path_property=LAM.path
                                        )
    constraints.make_triples()

    empty_lam_graph.serialize(destination=TEMP_OUTPUT_FOLDER / "constraint_lam_classes.ttl")

    assert (None, SH.hasValue, None) in empty_lam_graph
    assert (None, SH.name, None) in empty_lam_graph
    assert (None, LAM.hasPropertyConfiguration, None) in empty_lam_graph
    assert (None, LAM.path, None) in empty_lam_graph
    assert (None, SH.minCount, None) in empty_lam_graph
    assert (None, SH.maxCount, None) in empty_lam_graph
    assert (None, DCTERMS.created, None) in empty_lam_graph
    assert (None, SKOS.editorialNote, None) in empty_lam_graph
