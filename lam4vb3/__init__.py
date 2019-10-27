"""
__init__.py
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import pathlib

# Some path parameters

THIS_PROJECT = pathlib.Path(__file__).resolve().parent.parent

INPUT_EXCEL_FILE = (THIS_PROJECT / "docs/semi-structured/LAM_metadata_04_ECO.xlsx").resolve()

LAM_p = "lam_project_properties_v2.ttl"
LAM_c = "lam_project_classes_v2.ttl"
CELEX_c = "celex_project_classes_v2.ttl"
CELEX_p = "celex_project_properties_v2.ttl"

LAM_PROPERTIES_TTL = (THIS_PROJECT / "output" / LAM_p).resolve()
LAM_CLASSES_TTL = (THIS_PROJECT / "output" / LAM_c).resolve()
CELEX_CLASSES_TTL = (THIS_PROJECT / "output" / CELEX_c).resolve()
CELEX_PROPERTIES_TTL = (THIS_PROJECT / "output" / CELEX_p).resolve()

LAM_PROPERTIES_WS_NAME = "LAM metadata"
LAM_CLASSES_WS_NAME = "Classes complete"
CELEX_PROPERTIES_WS_NAME = "CELEX metadata"
CELEX_CLASSES_WS_NAME = "CELEX classes"
