"""
builder
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""
import pandas as pd
import rdflib
import shortuuid

from lam4vb3.builder import SHACL
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


def read_excel_worksheet(file_path, sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(file_path, sheet_name=sheet_name,
                       header=[0], na_values=[""], keep_default_na=False, dtype=str)
    df.fillna(value="", inplace=True)
    return df


def make_graph(df, prefix_column="prefix", uri_column="uri"):
    """
        init the LAM data graph

    :param uri_column: the column in df that contains base namespace URIs
    :param prefix_column: the column in df that provides prefixes to be used in qnames
    :param df: the data frame containing namespace defitions
    """
    graph = rdflib.Graph()

    graph.bind("skos", rdflib.namespace.SKOS)
    graph.bind("dct", rdflib.namespace.DCTERMS)
    graph.bind("sh", SHACL)

    graph.bind("rdf", rdflib.namespace.RDF)
    graph.bind("rdfs", rdflib.namespace.RDFS)
    graph.bind("xsd", rdflib.namespace.XSD)
    graph.bind("owl", rdflib.namespace.OWL)
    graph.bind("xml", rdflib.namespace.XMLNS)

    # normalise the prefixes read into a dataframe
    df.fillna("", inplace=True)
    namespace_mapping_dict = dict(zip(df[prefix_column], df[uri_column]))
    ns_dict = {str(k).replace(":", ""):
                   str(v).strip() if (str(v).endswith("/") or str(v).endswith("#"))
                   else str(str(k) + ":") for k, v in namespace_mapping_dict.items() if v}

    for k, v in ns_dict.items():
        graph.bind(k, rdflib.Namespace(v))

    return graph