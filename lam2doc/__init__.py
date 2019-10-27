"""
__init__.py
Date: 18.10.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import pathlib

CONCEPT_SCHEME_QNAME = "skos:ConceptScheme"
CONCEPT_QNAME = "skos:Concept"

THIS_PROJECT = pathlib.Path(__file__).resolve().parent.parent
HTML_TEMPLATE_FOLDER = (THIS_PROJECT / "doc_templates/html").resolve()
