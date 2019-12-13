"""
__init__.py
Date: 18.10.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import pathlib

CONCEPT_SCHEME_QNAME = "skos:ConceptScheme"
CONCEPT_QNAME = "skos:Concept"
COLLECTION_QNAME = "skos:Collection"


THIS_PROJECT = pathlib.Path(__file__).resolve().parent.parent
# HTML_TEMPLATE_FOLDER = (THIS_PROJECT / "doc_templates/html").resolve()
HTML_TEMPLATE_FOLDER = (pathlib.Path(__file__).resolve().parent / "doc_templates/html").resolve()

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

STATIC_FILES = (pathlib.Path(__file__).resolve().parent / "doc_templates/html_static").resolve()