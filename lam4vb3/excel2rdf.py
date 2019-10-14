""" 
excel2rdf
Created:  14/10/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import pathlib
import shutil

import build
import pandas as pd
import property_build
import class_build
import lam_utils
import click
import logging
import rdflib
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, OWL, XMLNS, XSD
from datetime import date
import time

# INPUT_FILE = pathlib.Path("../docs/semi-structured/LAM_metadata_03.xlsx").resolve()
INPUT_FILE = pathlib.Path("../docs/semi-structured/LAM_metadata_04_ECO.xlsx").resolve()
OUTPUT_FILE = pathlib.Path("../output/lam_project_v1.ttl").resolve()
OUTPUT_FILE_LAM_PROPERTIES = pathlib.Path("../output/lam_project_properties_v2.ttl").resolve()
OUTPUT_FILE_LAM_CLASSES = pathlib.Path("../output/lam_project_classes_v2.ttl").resolve()
OUTPUT_FILE_CELEX_CLASSES = pathlib.Path("../output/celex_project_classes_v2.ttl").resolve()
OUTPUT_FILE_CELEX_PROPERTIES = pathlib.Path("../output/celex_project_properties_v2.ttl").resolve()

LAM_PROPERTIES_WS_NAME = "LAM metadata"
LAM_CLASSES_WS_NAME = "Classes complete"
CELEX_PROPERTIES_WS_NAME = "CELEX metadata"
CELEX_CLASSES_WS_NAME = "CELEX classes"

LAM_p = "lam_project_properties_v2.ttl"
LAM_c = "lam_project_classes_v2.ttl"
CELEX_c = "celex_project_classes_v2.ttl"
CELEX_p = "celex_project_properties_v2.ttl"

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def transform_file(input_f, output_f):
    """
    :param output_f:
    :param input_f:
    :return:
    """
    input_file = pathlib.Path(input_f).resolve() if input_f else INPUT_FILE

    output_f = output_f / input_f.stem
    shutil.rmtree(output_f, ignore_errors=True)
    output_f.mkdir()

    logging.info(f"Opening the file {input_file}")

    # reading the input
    lam_df_properties = pd.read_excel(input_file, sheet_name=LAM_PROPERTIES_WS_NAME, header=[0], na_values=[""],
                                      keep_default_na=False)
    logging.info(f"Finished reading {len(lam_df_properties)} LAM property definitions")
    lam_df_classes = pd.read_excel(input_file, sheet_name=LAM_CLASSES_WS_NAME, header=[0], na_values=[""],
                                   keep_default_na=False)
    logging.info(f"Finished reading {len(lam_df_classes)} LAM class definitions")
    celex_df_properties = pd.read_excel(input_file, sheet_name=CELEX_PROPERTIES_WS_NAME, header=[0], na_values=[""],
                                        keep_default_na=False)
    logging.info(f"Finished reading {len(celex_df_properties)} CELEX property definitions")
    celex_df_classes = pd.read_excel(input_file, sheet_name=CELEX_CLASSES_WS_NAME, header=[0], na_values=[""],
                                     keep_default_na=False)
    logging.info(f"Finished reading {len(celex_df_classes)} CELEX class definitions")
    prefixes = pd.read_excel(input_file, sheet_name=4, header=[0], na_values=[""], keep_default_na=False)
    logging.info(f"Finished reading {len(prefixes)} Prefix definitions")
    # transforming and writing the output

    start_time = time.time()
    logging.info(f"Transforming the CELEX classes into RDF.")
    celex_df_classes['DTS'] = celex_df_classes['DTS'].apply(str)
    class_build.make_celex_class_worksheet(celex_df_classes, prefixes, output_f / CELEX_c)
    logging.info(
        f"Successfully completed the transformation. The output is written into {output_f / CELEX_c}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")

    start_time = time.time()
    logging.info(f"Transforming the CELEX properties into RDF.")
    property_build.make_property_worksheet(celex_df_properties, prefixes, output_f / CELEX_p)
    logging.info(
        f"Successfully completed the transformation. The output is written into {output_f / CELEX_p}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")

    start_time = time.time()
    logging.info(f"Transforming the LAM properties into RDF.")
    property_build.make_property_worksheet(lam_df_properties, prefixes, output_f / LAM_p)
    logging.info(f"Successfully completed the transformation. The output is written into {output_f / LAM_p}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")

    start_time = time.time()
    logging.info(f"Transforming the LAM classes into RDF.")
    class_build.make_class_worksheet(lam_df_classes, prefixes, output_f / LAM_c)
    logging.info(
        f"Successfully completed the transformation. The output is written into {output_f / LAM_c}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")

    start_time = time.time()


@click.command()
@click.argument("input", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument("output", type=click.Path(exists=True, file_okay=False, dir_okay=True))
def transform_files_in_folder(input, output):
    """
        takes all Excel files from an input folder, transforms them into LAM-SKOS-AP RDF
        and writes them into the output folder.
    :param input:
    :param output:
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
