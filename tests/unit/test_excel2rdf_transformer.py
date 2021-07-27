#!/usr/bin/python3

# test_excel2rdf_transformer.py
# Date:  27/07/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import shutil

from lam4vb3.excel2rdf import transform_properties
from tests import THIS_PROJECT, INPUT_EXCEL_FILE_TEST_DATA


def test_transform_sample_data_properties():
    """
        This test will simply run the transformation and assert the output files exist.
        The output file content will be checked elsewhere.
    :return:
    """
    output_folder = (THIS_PROJECT / "tests" / "output").resolve()
    input_file = INPUT_EXCEL_FILE_TEST_DATA
    shutil.rmtree(output_folder, ignore_errors=True)
    output_folder.mkdir()

    transform_properties(input_file=input_file, output_folder=output_folder)
    assert output_folder.exists()
    assert output_folder.is_dir()
    assert any(output_folder.iterdir())
