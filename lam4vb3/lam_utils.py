"""
builder
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import re


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


def normalise_namespace_mapping_dict(df, prefix_column="prefix", uri_column="uri"):
    """
        TODO: unify a common library, this function is taken from rdf finger-printer project

    :param namespace_mapping_dict:
    :return:
    """
    namespace_mapping_dict = (dict(zip(df[prefix_column], df[uri_column])))
    return {str(k).strip() if str(k).endswith(":") else str(str(k) + ":"): str(v).strip() for k, v in
            namespace_mapping_dict.items()}
