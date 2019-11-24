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
INPUT_EXCEL_FILE = (THIS_PROJECT / "docs" / "semi-structured" / "LAM_metadata_20191124_ECO.xlsx").resolve()

LAM_p = "lam_project_properties_v2.ttl"
LAM_c = "lam_project_classes_v2.ttl"
CELEX_c = "celex_project_classes_v2.ttl"

LAM_PROPERTIES_TTL = (THIS_PROJECT / "data" / LAM_p).resolve()
LAM_CLASSES_TTL = (THIS_PROJECT / "data" / LAM_c).resolve()
CELEX_CLASSES_TTL = (THIS_PROJECT / "data" / CELEX_c).resolve()

LAM_PROPERTIES_WS_NAME = "LAM properties"
LAM_CLASSES_WS_NAME = "LAM classes"
LAM_PROPERTY_CLASSIFICATION = "LAM property classification"
CELEX_CLASSES_WS_NAME = "CELEX classes"
PREFIX_WS_NAME = "prefixes"
