import rdflib
from rdflib import SH

from lam4vb3.builder import LAM, AT, LAMD
from lam4vb3.builder.reified_builders import ConstraintTripleMaker
from tests.unit.conftest import TEMP_OUTPUT_FOLDER

URI_COLUMN = 'URI'

CONSTRAINT_COLUMNS = {
    "ANN_COD": "lamd:md_ANN_COD",
    "ANN_TOD": "lamd:md_ANN_TOD",
    "ANN_ART": "lamd:md_ANN_ART",
}


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
