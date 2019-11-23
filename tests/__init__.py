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

THIS_PROJECT = pathlib.Path(__file__).resolve().parent.parent

LAM_HELLO_WORLD_HTML = (THIS_PROJECT / "data/lam_hello_world.html").resolve()

