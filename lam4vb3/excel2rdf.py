""" 
excel2rdf
Created:  14/10/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import pathlib
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


@click.command()
@click.option('--input_f', help='The path to input file')
def transform(input_f=None):
    """
    :param input_f:
    :return:
    """
    input_file = pathlib.Path(input_f).resolve() if input_f else INPUT_FILE

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

    logging.info(f"Transforming the LAM properties into RDF.")
    property_build.make_property_worksheet(lam_df_properties, prefixes, OUTPUT_FILE_LAM_PROPERTIES)
    logging.info(f"Successfully completed the transformation. The output is written into {OUTPUT_FILE_LAM_PROPERTIES}")

    logging.info(f"Transforming the LAM classes into RDF.")
    class_build.make_class_worksheet(lam_df_classes, prefixes, OUTPUT_FILE_LAM_CLASSES)
    logging.info(
        f"Successfully completed the transformation. The output is written into {OUTPUT_FILE_LAM_CLASSES}")

    logging.info(f"Transforming the CELEX classes into RDF.")
    celex_df_classes['DTS'] = celex_df_classes['DTS'].apply(str)
    class_build.make_celex_class_worksheet(celex_df_classes, prefixes, OUTPUT_FILE_CELEX_CLASSES)
    logging.info(
        f"Successfully completed the transformation. The output is written into {OUTPUT_FILE_CELEX_CLASSES}")

    logging.info(f"Transforming the CELEX properties into RDF.")
    property_build.make_property_worksheet(celex_df_properties, prefixes, OUTPUT_FILE_CELEX_PROPERTIES)
    logging.info(
        f"Successfully completed the transformation. The output is written into {OUTPUT_FILE_CELEX_PROPERTIES}")


if __name__ == '__main__':
    transform()
