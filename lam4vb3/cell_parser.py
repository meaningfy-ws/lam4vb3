"""
This module implements Excel cell parsing as define in the excel srtucture specification document.

cases:

1. Literal values
2. Cardinality values with comments
3. Multi line reference values with comments

"""
import re

import pandas as pd
import rdflib

LITERAL_VALUE = "literal_value"
VALUES = "values"
COMMENT = "comment"
MIN_COUNT = "min_count"
MAX_COUNT = "max_count"
NAME = "name"

CONTROLLED_LIST = {
    "y": {MIN_COUNT: 1, NAME: "Mandatory"},
    "yu": {MIN_COUNT: 1, MAX_COUNT: 1, NAME: "Mandatory unique"},
    "": {},
    "ou": {MAX_COUNT: 1},
    "o": {},
    "n": {MAX_COUNT: 0, NAME: "Forbidden"},
}


def parse_cell(cell_value: str, graph: rdflib.Graph, is_literal=False) -> dict:
    """
        Interpret the cell_value if it is not a literal.
        The interpretation can be for cardinality constaint or value constraint.
        returns a dict possibly containing the following structure
        {
            literal_value: 'the literal value',
            min_count:int,
            max_count:int,
            values: [<list of URIs>],
            comment: 'comment literal'
        }

    """
    result = {}
    if is_literal:
        if cell_value == "":
            return result
        else:
            return {LITERAL_VALUE: cell_value}
        # else:
        #     raise ValueError(
        #         f"Literal values should be free text with no markers present (|). The value given was {cell_value}")

    first_part, second_part = split_by_pipe(cell_value)
    first_part = normalize_spaces(first_part)

    if second_part:
        result[COMMENT] = second_part

    if first_part.lower() in CONTROLLED_LIST:
        result.update(CONTROLLED_LIST[first_part.lower()])
    else:
        values = split_lines(first_part)
        list_of_uris = [qname_uri(qname, graph.namespaces()) for qname in values]
        result[VALUES] = list_of_uris
        result[MIN_COUNT] = 1

    return result


def split_by_pipe(string: str) -> tuple:
    """
        For a given cell_value (string) split the string by pipe ("|") an return a
        list a values. It will raise an error if there are more than on pipe
    """
    pipe = " | "
    result_list = string.split(pipe)
    if len(result_list) > 2:
        raise ValueError(f"Cannot have more than one pipe (|) separator in the cell value")

    return result_list[0], result_list[1] if len(result_list) > 1 else None


def split_lines(string: str) -> list:
    return list(filter(None, [normalize_spaces(x) for x in string.split("\n")]))


def normalize_spaces(string: str):
    if string:
        return re.sub(" +", " ", string).lstrip().rstrip()
    return string


def parse_qname(qname):
    """
        give a qualified name such as skos:prefLabel (or skos:prefLabel@en with linguistic annotation)
    """
    p = re.compile(r"""([\w\-_]+){0,1}:([\w\-_]+){1,1}(?:@){0,1}([\w]+){0,1}""")
    try:
        dummy1, prefix, name, language, dummy2 = p.split(qname)
    except:
        raise ValueError(f"Could not segment the qualified name: {qname}")
    return "" if prefix is None else prefix, name, language


def qname_uri(qname, namespaces):
    """
        return the URI for this qname provided that the prefix is found in the list of namescapce tuples
    """
    prefix, name, language = parse_qname(qname)
    try:
        base = [ns for ns in namespaces if ns[0] == prefix][0][1]
    except:
        raise ValueError(f"Invalid or unknown qualified name: {qname}. Parsed as {prefix}:{name}@{language}")
    return base + name


def qname_lang(qname):
    """
        return the language of this qname provided that the prefix is found in the list of namescapce tuples
    """
    return parse_qname(qname)[2]


def parse_value(value, graph=None, language=None, data_type=None):
    """
    //TODO : deprecate
        create a resource either as URI or Literal
    :param value:
    :param graph:
    :param language:
    :param data_type:
    :return: URIRef or Literal
    """
    if value and not pd.isna(value):
        if graph is not None:
            try:
                return qname_uri(str.strip(value), graph.namespaces())
            except Exception:
                return rdflib.URIRef(str.strip(value))
        elif language:
            return rdflib.Literal(value, lang=language)
        elif data_type:
            return rdflib.Literal(value, datatype=data_type)
        else:
            return rdflib.Literal(value)


def parse_multi_line_value(multi_line_value, graph=None, language=None, data_type=None):
    """
    //TODO : deprecate
    :param multi_line_value:
    :param graph:
    :param language:
    :param data_type:
    :return:
    """
    return [parse_value(x, graph=graph, language=language, data_type=data_type)
            for x in re.split(r"[\n,]", multi_line_value) if x]


def parse_commented_value(commented_value, graph=None, language=None, data_type=None) -> (
        "cell value", "cell comment"):
    """
        //TODO : deprecate

        return the tuple (value,comment) spiting the cell_value into the actual value and the comment,
        which is the part after the special character pipe (|) or tilda (~). If no comment is provided None is returned

        examples:
            value1 | with a comment
            value2 ~ with another comment

    :param data_type:
    :param language:
    :param graph: should the value be interpreted as URI, then use this graph for name space intepretation
    :param commented_value: the string value of the cell
    :return: tuple("cell value", "cell comment")
    """
    parts = [x for x in re.split(r"[~\|]", commented_value) if x]
    value = parts[0] if parts else None
    comment = parts[1] if len(parts) > 1 else None
    parsed_value = parse_value(value, graph=graph, language=language, data_type=data_type)
    parsed_comment = parse_value(comment, language=language, )
    return parsed_value, parsed_comment


def parse_multi_line_commented_value(multi_line_commented_value, graph=None, language=None,
                                     data_type=None) -> [("cell value", "cell comment")]:
    """
     //TODO : deprecate

        return a list of tuples where each tuple is a (value,comment) split
    :param multi_line_commented_value:
    :param graph:
    :param language:
    :param data_type:
    :return:
    """

    lines = [str.strip(x) for x in re.split(r"\n", multi_line_commented_value) if x]
    return [parse_commented_value(x, graph=graph, language=language, data_type=data_type) for x in lines
            if x]
