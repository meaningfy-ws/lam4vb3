"""
builder
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import shortuuid

from lam4vb3.cell_parser import qname_uri

URI_UUID_PREFIX = "res_"
URI_UUID_SUFFIX = ""


def generate_uuid_uri(value, graph, seed="", prefix=URI_UUID_PREFIX, suffix=URI_UUID_SUFFIX):
    local_uid = shortuuid.uuid(name=str(seed) + str(value))
    qname = ":" + str(prefix).strip() + str(local_uid) + str(suffix).strip()
    return qname_uri(qname, graph.namespaces())


def add_triples_to_graph(result_triples, graph):
    """
        just add the triples to a graph
    :return:
    """
    for triple in result_triples:
        graph.add(triple)