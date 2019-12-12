"""
rdf2json.py
Date: 12/12/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""
import logging
import pathlib
import time

import click

from lam2doc.content_generator import LAMGremlinGenerator


@click.command(name="rdf2json", help="Takes a SKOS file and turns it into a JSON document so that it can be used as "
                                     "structured data source for document generation.\nNote: This operation requires a"
                                     "Gremlin service to run locally.")
@click.argument("input_file", type=click.Path(exists=True, file_okay=True))
@click.argument("output_folder", type=click.Path(dir_okay=True))
@click.option("--format", "-f", "frm", default="json", type=click.Choice(['json', 'xml'], ))
@click.option("--generate-collections", "-c", "generate_collections", is_flag=True,
              help="By default the JSON will contains Concepts and Concept Schemes. If you want to add Collections as "
                   "well use this flag.")
def transform(input_file, output_folder, generate_collections, frm):
    """

    """
    in_ = pathlib.Path(input_file).resolve()
    out_ = pathlib.Path(output_folder).resolve()
    out_.mkdir(exist_ok=True)
    out_file_ = (out_ / in_.stem).with_suffix("."+frm)

    start_time = time.time()
    gen = LAMGremlinGenerator(str(input_file), generate_collections=generate_collections)
    if frm == "json":
        gen.to_json(str(out_file_))
    elif frm == "xml":
        gen.to_xml(str(out_file_))
    else:
        raise Exception(f"Unknown format {format}")

    logging.info(f"Successfully completed the transformation. The output is written into {out_}")
    logging.info(f"Elapsed {(time.time() - start_time)} seconds")


if __name__ == '__main__':
    transform()
