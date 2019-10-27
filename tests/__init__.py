"""
__init__.py
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import pathlib

THIS_PROJECT = pathlib.Path(__file__).resolve().parent.parent

LAM_PROPERTY_EXAMPLE = (THIS_PROJECT / "output/lam_project_properties_v2.ttl").resolve()
LAM_CLASS_EXAMPLE = (THIS_PROJECT / "output/lam_project_classes_v2.ttl").resolve()

LAM_PROPERTY_CONTENT_JSON = (THIS_PROJECT / "output/lam_project_properties.json").resolve()
LAM_PROPERTY_CONTENT_XML = (THIS_PROJECT / "output/lam_project_properties.xml").resolve()
LAM_CLASS_CONTENT_JSON = (THIS_PROJECT / "output/lam_project_classes.json").resolve()


LAM_HELLO_WORLD_HTML = (THIS_PROJECT / "output/lam_hello_world.html").resolve()

LAM_PROPERTIES_HTML = (THIS_PROJECT / "output/lam_properties.html").resolve()
LAM_CLASSES_HTML = (THIS_PROJECT / "output/lam_classes.html").resolve()


