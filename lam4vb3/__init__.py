"""
__init__.py
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import logging
import pathlib

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# Some path parameters

THIS_PROJECT = pathlib.Path(__file__).resolve().parent.parent

# INPUT_EXCEL_FILE = (THIS_PROJECT / "docs" / "semi-structured" / "LAM_metadata_04_ECO.xlsx").resolve()
# INPUT_EXCEL_FILE = (THIS_PROJECT / "docs" / "semi-structured" / "LAM_metadata_20191120_ECO.xlsx").resolve()
# INPUT_EXCEL_FILE = (THIS_PROJECT / "docs" / "semi-structured" / "LAM_metadata_20191124_ECO.xlsx").resolve()
# INPUT_EXCEL_FILE = (THIS_PROJECT / "docs" / "semi-structured" / "LAM_metadata_20191209_JKU.xlsx").resolve()
INPUT_EXCEL_FILE = (THIS_PROJECT / "docs" / "semi-structured" / "LAM_metadata_20200903_JKU.xlsx").resolve()

LAM_p = "lam_project_properties_v2.ttl"
LAM_c = "lam_project_classes_v2.ttl"
CELEX_c = "celex_project_classes_v2.ttl"

LAM_PROPERTIES_TTL = (THIS_PROJECT / "data" / LAM_p).resolve()
LAM_CLASSES_TTL = (THIS_PROJECT / "data" / LAM_c).resolve()
CELEX_CLASSES_TTL = (THIS_PROJECT / "data" / CELEX_c).resolve()

LAM_PROPERTIES_WS_NAME = "LAM properties"
LAM_PROPERTY_CLASSIFICATION_WS_NAME = "LAM property classification"

LAM_CLASSES_WS_NAME = "LAM classes"
LAM_CLASS_CLASSIFICATION_WS_NAME = "LAM class classification"

CELEX_CLASSES_WS_NAME = "CELEX classes"
# CELEX_CLASS_CLASSIFICATION_WS_NAME = "CELEX class classification"
CELEX_CLASS_CLASSIFICATION_WS_NAME = "CELEX classes classification"

PREFIX_WS_NAME = "prefixes (aux)"
