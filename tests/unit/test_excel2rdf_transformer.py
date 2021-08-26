#!/usr/bin/python3

# test_excel2rdf_transformer.py
# Date:  27/07/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import shutil

from lam4vb3.builder.property_builder import make_property_worksheet
from lam4vb3.builder.lam_classes_builder import make_lam_classes_worksheet
from lam4vb3.builder.celex_classes_builder import make_celex_classes_worksheet
from tests import THIS_PROJECT, OUTPUT_FOLDER

shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
OUTPUT_FOLDER.mkdir()


def test_transform_sample_data_properties(test_lam_properties_df, test_lam_properties_classification_df,
                                          test_prefixes_df, empty_lam_graph):
    """
        This test will simply run the transformation and assert the output files exist.
        The output file content will be checked elsewhere.
    :return:
    """

    output_folder = (THIS_PROJECT / "tests" / "output").resolve()
    shutil.rmtree(output_folder, ignore_errors=True)
    output_folder.mkdir()
    make_property_worksheet(lam_df_properties=test_lam_properties_df,
                            lam_df_property_classification=test_lam_properties_classification_df,
                            prefixes=test_prefixes_df, output_file=output_folder / "lam_properties.ttl")

    assert output_folder.exists()
    assert output_folder.is_dir()
    assert any(output_folder.iterdir())


def test_transform_sample_data_classes(test_lam_classes_df, test_lam_classes_classification_df,
                                       test_prefixes_df, empty_lam_graph):
    """
        This test will simply run the transformation and assert the output files exist.
        The output file content will be checked elsewhere.
    :return:
    """
    output_folder = (THIS_PROJECT / "tests" / "output").resolve()
    shutil.rmtree(output_folder, ignore_errors=True)
    output_folder.mkdir()
    make_lam_classes_worksheet(lam_df_classes=test_lam_classes_df,
                               lam_df_classes_classification=test_lam_classes_classification_df,
                               prefixes=test_prefixes_df, output_file=output_folder / "lam_classes.ttl")
    # transform_properties(input_file=input_file, output_folder=output_folder)
    assert output_folder.exists()
    assert output_folder.is_dir()
    assert any(output_folder.iterdir())


def test_transform_sample_data_celex_classes(test_lam_celex_classes_df, test_lam_celex_classes_classification_df,
                                             test_prefixes_df, empty_lam_graph):
    """
        This test will simply run the transformation and assert the output files exist.
        The output file content will be checked elsewhere.
    :return:
    """
    output_folder = (THIS_PROJECT / "tests" / "output").resolve()
    shutil.rmtree(output_folder, ignore_errors=True)
    output_folder.mkdir()
    make_celex_classes_worksheet(lam_df_celex_classes=test_lam_celex_classes_df,
                                 lam_df_celex_classes_classification=test_lam_celex_classes_classification_df,
                                 prefixes=test_prefixes_df, output_file=output_folder / "celex_classes.ttl")
    # transform_properties(input_file=input_file, output_folder=output_folder)
    assert output_folder.exists()
    assert output_folder.is_dir()
    assert any(output_folder.iterdir())
