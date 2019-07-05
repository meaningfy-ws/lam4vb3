"""
builder
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import re

import shortuuid


def parse_qname(qname):
    """
        give a qualified name such as skos:prefLabel (or skos:prefLabel@en with linguistic annotation) 
    """
    p = re.compile(r"""([\w]+){0,1}:([\w\-_]+){1,1}(?:@){0,1}([\w]+){0,1}""")
    try:
        dummy1, prefix, name, language, dummy2 = p.split(qname)
    except:
        raise Exception(f"Could not segment the qualified name: {qname}")
    return "" if prefix is None else prefix, name, language


def qname_uri(qname, namespaces):
    """
        return the URI for this qname provided that the prefix is found in the list of namescapce tuples 
    """
    prefix, name, language = parse_qname(qname)
    try:
        base = [ns for ns in namespaces if ns[0] == prefix][0][1]
    except:
        raise Exception(f"Invalid or unknown qualified name: {qname}")
    return base + name


def qname_lang(qname):
    """
        return the language of this qname provided that the prefix is found in the list of namescapce tuples 
    """
    return parse_qname(qname)[2]


def generate_uuid_uri(value, graph, seed="", prefix="", suffix=""):
    local_uid = shortuuid.uuid(name=str(seed) + str(value))
    qname = ":" + str(prefix).strip() + str(local_uid) + str(suffix).strip()
    return qname_uri(qname, graph.namespaces())
