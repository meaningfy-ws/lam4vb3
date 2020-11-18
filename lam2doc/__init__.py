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
STATIC_FILES = (pathlib.Path(__file__).resolve().parent / "doc_templates/html_static").resolve()