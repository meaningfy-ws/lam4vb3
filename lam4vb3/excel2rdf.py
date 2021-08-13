""" 
excel2rdf
Created:  14/10/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import pathlib
import warnings

import pandas as pd
import click
import logging
import time

from lam4vb3 import LAM_PROPERTIES_WS_NAME, LAM_CLASSES_WS_NAME, CELEX_CLASSES_WS_NAME, \
    LAM_PROPERTY_CLASSIFICATION_WS_NAME, PREFIX_WS_NAME, \
    LAM_CLASS_CLASSIFICATION_WS_NAME, CELEX_CLASS_CLASSIFICATION_WS_NAME
from lam4vb3.builder.celex_classes_builder import make_celex_classes_worksheet
from lam4vb3.builder.lam_classes_builder import make_lam_classes_worksheet
from lam4vb3.builder.property_builder import make_property_worksheet
from lam4vb3.lam_utils import read_excel_worksheet
from tests import LAM_p, LAM_c, CELEX_c


def transform_properties(input_file, output_folder):
    logging.info(f"Transforming LAM properties from  the file {input_file}")

    lam_df_properties = read_excel_worksheet(file_path=input_file, sheet_name=LAM_PROPERTIES_WS_NAME)
    lam_df_property_classification = read_excel_worksheet(file_path=input_file,
                                                          sheet_name=LAM_PROPERTY_CLASSIFICATION_WS_NAME)
    prefixes = read_excel_worksheet(file_path=input_file, sheet_name=PREFIX_WS_NAME)

    start_time = time.time()
    return_graph = make_property_worksheet(lam_df_properties=lam_df_properties,
                                           lam_df_property_classification=lam_df_property_classification,
                                           prefixes=prefixes, output_file=pathlib.Path(output_folder) / LAM_p)

    logging.info(
        f"Successfully completed the transformation. The output is written into {pathlib.Path(output_folder) / LAM_p}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")
    return return_graph


def transform_classes(input_file, output_folder):
    logging.info(f"Transforming LAM classes classes from the file {input_file}")
    lam_df_classes = read_excel_worksheet(file_path=input_file, sheet_name=LAM_CLASSES_WS_NAME)
    lam_df_classes_classification = read_excel_worksheet(file_path=input_file,
                                                         sheet_name=LAM_CLASS_CLASSIFICATION_WS_NAME)
    prefixes = read_excel_worksheet(file_path=input_file, sheet_name=PREFIX_WS_NAME)

    start_time = time.time()
    returned_graph = make_lam_classes_worksheet(lam_df_classes=lam_df_classes,
                                                lam_df_classes_classification=lam_df_classes_classification,
                                                prefixes=prefixes, output_file=pathlib.Path(output_folder) / LAM_c)
    logging.info(
        f"Successfully completed the transformation. The output is written into {pathlib.Path(output_folder) / LAM_c}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")
    return returned_graph


def transform_celex_classes(input_file, output_folder):
    logging.info(f"Transforming CELEX classes from the file {input_file}")
    celex_df_classes = read_excel_worksheet(file_path=input_file, sheet_name=CELEX_CLASSES_WS_NAME)
    celex_df_class_classification = read_excel_worksheet(file_path=input_file,
                                                         sheet_name=CELEX_CLASS_CLASSIFICATION_WS_NAME)
    prefixes = read_excel_worksheet(file_path=input_file, sheet_name=PREFIX_WS_NAME)

    start_time = time.time()
    returned_graph = make_celex_classes_worksheet(lam_df_celex_classes=celex_df_classes,
                                                  lam_df_celex_classes_classification=celex_df_class_classification,
                                                  prefixes=prefixes,
                                                  output_file=pathlib.Path(output_folder) / CELEX_c)
    logging.info(
        f"Successfully completed the transformation. The output is written into {pathlib.Path(output_folder) / CELEX_c}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")
    return returned_graph


@click.command()
@click.argument("input", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument("output", type=click.Path(exists=True, file_okay=False, dir_okay=True))
def transform_files_in_folder(input, output):
    """
        takes all Excel files from an input folder, transforms them into LAM-SKOS-AP RDF
        and writes them into the output folder.
    :param input: the folder with excel files
    :param output: the folder with RDF files
    :return:
    """
    warnings.warn("deprecated", DeprecationWarning)

    in_ = pathlib.Path(input).resolve()
    out_ = pathlib.Path(output).resolve()

    file_list = list(in_.glob("*.xlsx*"))

    logging.info(f"Input: {in_}")
    logging.info(f"Output: {out_}")
    logging.info(f"Executing the transformation for each Excel file (*.xlsx) in the input folder")

    # logging.info(f"Files: {file_list}")

    for file_path in file_list:
        logging.info(f"> Transforming {file_path.name}")
        try:
            transform(file_path, out_)
        except Exception:
            logging.exception("Could not transform the file. Most likely it does not respect "
                              "the conventions. Please update and try again. ", exc_info=True)


@click.command()
@click.argument("input_file", type=click.Path(exists=True, file_okay=True))
@click.argument("output_folder", type=click.Path(exists=True, dir_okay=True))
def transform(input_file, output_folder):
    """
        Transform a given file and write the output into a folder.
    """
    in_ = pathlib.Path(input_file).resolve()
    out_ = pathlib.Path(output_folder).resolve()

    logging.info(f"Input: {in_}")
    logging.info(f"Output: {out_}")

    out_.mkdir(exist_ok=True)

    logging.info(f"> Transforming {in_.name}")

    transform_celex_classes(in_, out_)
    transform_properties(in_, out_)
    transform_classes(in_, out_)


if __name__ == '__main__':
    transform()
