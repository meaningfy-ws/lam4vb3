""" 
excel2rdf
Created:  14/10/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import pathlib
import shutil

import pandas as pd
import click
import logging
import time

from lam4vb3 import LAM_PROPERTIES_WS_NAME, LAM_CLASSES_WS_NAME, CELEX_CLASSES_WS_NAME, \
    class_build, CELEX_c, LAM_p, LAM_c, property_build, LAM_PROPERTY_CLASSIFICATION


def transform_file(input_file, output_folder):
    """
    :param output_folder:
    :param input_file:
    :return:
    """
    # input_file = pathlib.Path(input_file).resolve() if input_file else INPUT_FILE

    output_folder = output_folder / input_file.stem
    shutil.rmtree(output_folder, ignore_errors=True)
    output_folder.mkdir()

    logging.info(f"Opening the file {input_file}")

    # reading the input
    lam_df_properties = pd.read_excel(str(input_file), sheet_name=LAM_PROPERTIES_WS_NAME, header=[0], na_values=[""],
                                      keep_default_na=False)
    logging.info(f"Finished reading {len(lam_df_properties)} LAM property definitions")
    lam_df_classes = pd.read_excel(input_file, sheet_name=LAM_CLASSES_WS_NAME, header=[0], na_values=[""],
                                   keep_default_na=False)
    logging.info(f"Finished reading {len(lam_df_classes)} LAM class definitions")
    # celex_df_properties = pd.read_excel(input_file, sheet_name=CELEX_PROPERTIES_WS_NAME, header=[0], na_values=[""],
    #                                     keep_default_na=False)
    # logging.info(f"Finished reading {len(celex_df_properties)} CELEX property definitions")
    celex_df_classes = pd.read_excel(input_file, sheet_name=CELEX_CLASSES_WS_NAME, header=[0], na_values=[""],
                                     keep_default_na=False)
    logging.info(f"Finished reading {len(celex_df_classes)} CELEX class definitions")
    prefixes = pd.read_excel(input_file, sheet_name=4, header=[0], na_values=[""], keep_default_na=False)
    logging.info(f"Finished reading {len(prefixes)} Prefix definitions")

    lam_df_property_classification = pd.read_excel(input_file, sheet_name=LAM_PROPERTY_CLASSIFICATION, header=[0],
                                                   na_values=[""], keep_default_na=False)
    logging.info(f"Finished reading {len(lam_df_property_classification)} LAM property classification definitions")
    # transforming and writing the output

    start_time = time.time()
    logging.info(f"Transforming the CELEX classes into RDF.")
    celex_df_classes['DTS'] = celex_df_classes['DTS'].apply(str)
    celex_df_classes['CODE'] = celex_df_classes['CODE'].apply(str)
    class_build.make_celex_class_worksheet(celex_df_classes, prefixes, output_folder / CELEX_c)
    logging.info(
        f"Successfully completed the transformation. The output is written into {output_folder / CELEX_c}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")

    start_time = time.time()
    logging.info(f"Transforming the LAM properties into RDF.")
    property_build.make_property_worksheet(lam_df_properties, lam_df_property_classification, prefixes,
                                           output_folder / LAM_p)
    logging.info(f"Successfully completed the transformation. The output is written into {output_folder / LAM_p}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")

    start_time = time.time()
    logging.info(f"Transforming the LAM classes into RDF.")
    class_build.make_class_worksheet(lam_df_classes, prefixes, output_folder / LAM_c)
    logging.info(
        f"Successfully completed the transformation. The output is written into {output_folder / LAM_c}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")
    start_time = time.time()


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
            transform_file(file_path, out_)
        except Exception:
            logging.exception("Could not transform the file. Most likely it does not respect "
                              "the conventions. Please update and try again. ", exc_info=True)
        logging.info(f"> Moving the input file {file_path.name} into the output folder {out_} ")
        shutil.move(str(file_path), str(out_))


if __name__ == '__main__':
    transform_files_in_folder()
