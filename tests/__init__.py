"""
__init__.py
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import logging
import pathlib

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

THIS_PROJECT = pathlib.Path(__file__).resolve().parent.parent

INPUT_EXCEL_FILE = (THIS_PROJECT / "tests" / "test_data" / "LAM_metadata_20200903_JKU.xlsx").resolve()
INPUT_EXCEL_FILE_TEST_DATA = (THIS_PROJECT / "tests" / "test_data" / "LAM_metadata_20210413_testbed.xlsx").resolve()

LAM_p = "lam_project_properties_v2.ttl"
LAM_c = "lam_project_classes_v2.ttl"
CELEX_c = "celex_project_classes_v2.ttl"

LAM_PROPERTIES_TTL = (THIS_PROJECT / "data" / LAM_p).resolve()
LAM_CLASSES_TTL = (THIS_PROJECT / "data" / LAM_c).resolve()
CELEX_CLASSES_TTL = (THIS_PROJECT / "data" / CELEX_c).resolve()

# lam2doc variables
LAM_HELLO_WORLD_HTML = (THIS_PROJECT / "data/lam_hello_world.html").resolve()

LAM_PROPERTIES_JSON = (THIS_PROJECT / "data/lam_project_properties_v2.json").resolve()
LAM_CLASSES_JSON = (THIS_PROJECT / "data/lam_project_classes_v2.json").resolve()
CELEX_CLASSES_JSON = (THIS_PROJECT / "data/celex_project_classes_v2.json").resolve()
LAM_PROPERTIES_XML = (THIS_PROJECT / "data/lam_project_properties_v2.xml").resolve()
LAM_CLASSES_XML = (THIS_PROJECT / "data/lam_project_classes_v2.xml").resolve()
CELEX_CLASSES_XML = (THIS_PROJECT / "data/celex_project_classes_v2.xml").resolve()
LAM_PROPERTIES_HTML = (THIS_PROJECT / "data/lam_project_properties_v2.html").resolve()
LAM_CLASSES_HTML = (THIS_PROJECT / "data/lam_project_classes_v2.html").resolve()
CELEX_CLASSES_HTML = (THIS_PROJECT / "data/celex_project_classes_v2.html").resolve()
LAM_OWL_TTL = (THIS_PROJECT / "data/lam_project_ontology.ttl").resolve()
LAM_OWL_HTML = (THIS_PROJECT / "data/lam_project_ontology.html").resolve()

OUTPUT_FOLDER = (THIS_PROJECT / "tests" / "output").resolve()