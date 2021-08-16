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
    class_build, property_build, LAM_PROPERTY_CLASSIFICATION_WS_NAME, PREFIX_WS_NAME, \
    LAM_CLASS_CLASSIFICATION_WS_NAME, CELEX_CLASS_CLASSIFICATION_WS_NAME
from tests import LAM_p, LAM_c, CELEX_c


def transform_properties(input_file, output_folder):
    logging.info(f"Transforming LAM properties from  the file {input_file}")
    lam_df_properties = pd.read_excel(input_file, sheet_name=LAM_PROPERTIES_WS_NAME,
                                      header=[0], na_values=[""], keep_default_na=False)
    logging.info(f"Finished reading {len(lam_df_properties)} LAM property definitions")

    lam_df_property_classification = pd.read_excel(input_file,
                                                   sheet_name=LAM_PROPERTY_CLASSIFICATION_WS_NAME,
                                                   header=[0], na_values=[""], keep_default_na=False)
    logging.info(f"Finished reading {len(lam_df_property_classification)} LAM property classifications")

    prefixes = pd.read_excel(input_file, sheet_name=PREFIX_WS_NAME,
                             header=[0], na_values=[""], keep_default_na=False)

    start_time = time.time()
    return_graph = property_build.make_property_worksheet(lam_df_properties, lam_df_property_classification, prefixes,
                                           pathlib.Path(output_folder) / LAM_p)
    logging.info(f"Successfully completed the transformation. The output is written into {pathlib.Path(output_folder) / LAM_p}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")
    return return_graph


def transform_classes(input_file, output_folder):
    logging.info(f"Transforming LAM classes classes from the file {input_file}")
    lam_df_classes = pd.read_excel(input_file, sheet_name=LAM_CLASSES_WS_NAME,
                                   header=[0], na_values=[""], keep_default_na=False)
    logging.info(f"Finished reading {len(lam_df_classes)} LAM class definitions")

    lam_df_class_classification = pd.read_excel(input_file,
                                                sheet_name=LAM_CLASS_CLASSIFICATION_WS_NAME,
                                                header=[0], na_values=[""], keep_default_na=False)
    logging.info(f"Finished reading {len(lam_df_class_classification)} LAM class classifications")

    prefixes = pd.read_excel(input_file, sheet_name=PREFIX_WS_NAME,
                             header=[0], na_values=[""], keep_default_na=False)

    start_time = time.time()

    returned_graph = class_build.make_class_worksheet(lam_df_classes, lam_df_class_classification, prefixes,
                                     pathlib.Path(output_folder) / LAM_c)
    logging.info(f"Successfully completed the transformation. The output is written into {pathlib.Path(output_folder) / LAM_c}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")
    return returned_graph


def transform_celex_classes(input_file, output_folder):
    logging.info(f"Transforming CELEX classes from the file {input_file}")
    celex_df_classes = pd.read_excel(input_file, sheet_name=CELEX_CLASSES_WS_NAME, header=[0],
                                     na_values=[""],
                                     dtype={"DTS": str, "CODE": str, },
                                     keep_default_na=False)
    logging.info(f"Finished reading {len(celex_df_classes)} CELEX class definitions")

    celex_df_class_classification = pd.read_excel(input_file,
                                                  sheet_name=CELEX_CLASS_CLASSIFICATION_WS_NAME,
                                                  dtype={"COMMENT": str, "DESCRIPTION": str, "ORDER": str,
                                                         "PARENT": str},
                                                  header=[0], na_values=[""], keep_default_na=False)
    logging.info(f"Finished reading {len(celex_df_class_classification)} CELEX class classifications")

    prefixes = pd.read_excel(input_file, sheet_name=PREFIX_WS_NAME,
                             header=[0], na_values=[""], keep_default_na=False)
    logging.info(f"Finished reading {len(prefixes)} prefixes")

    start_time = time.time()
    returned_graph = class_build.make_celex_class_worksheet(celex_df_classes, celex_df_class_classification, prefixes,
                                                            pathlib.Path(output_folder) / CELEX_c)
    logging.info(f"Successfully completed the transformation. The output is written into {pathlib.Path(output_folder) / CELEX_c}")
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
        # logging.info(f"> Moving the input file {file_path.name} into the output folder {out_} ")
        # shutil.move(str(file_path), str(out_))


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
