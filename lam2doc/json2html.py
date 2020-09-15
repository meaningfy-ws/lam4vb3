"""
json2html.py
Date: 12/12/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""
import json
import logging
import pathlib
import shutil
import time
import click

from lam2doc import STATIC_FILES
from lam2doc.document_generator import JinjaGenerator

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


@click.command(name="json2html",
               help="Takes a JSON file and turns it into a HTML document following a prepared template.")
@click.argument("input_file", type=click.Path(exists=True, file_okay=True))
# @click.argument("output_folder", type=click.Path(dir_okay=True))
@click.option("--template", "-t", "template", default="lam_properties",
              type=click.Choice(['lam_properties', 'lam_classes', 'celex_classes'], ))
def transform(input_file, template):
    """

    """
    in_ = pathlib.Path(input_file).resolve()
    out_ = in_.parent / in_.stem
    out_file_ = out_ / "main.html"  # (out_ / in_.stem).with_suffix("." + frm)

    # add the static files
    shutil.rmtree(out_, ignore_errors=True)
    shutil.copytree(STATIC_FILES, out_)

    start_time = time.time()
    with in_.open("r") as file_:
        properties_data = json.load(file_)
        gen = JinjaGenerator(main_template_name=template + ".html", data=properties_data)
        gen.serialise(out_file_)

    logging.info(f"Successfully completed the transformation. The output is written into {out_}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")


if __name__ == '__main__':
    transform()
