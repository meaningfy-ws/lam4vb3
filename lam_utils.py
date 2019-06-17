
import rdflib as rdf
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, FOAF, OWL, XMLNS, XSD
import pathlib
import pandas as pd
import re 
import lam_utils
import warnings


def multiindex_colum_header(multiindex, top_column_name):
    """
        get the names of column headers at each level of the multiindex
    """
    # find column position
    column_position = multiindex.get_level_values(0).get_loc(top_column_name)
    # get header values at each level of the index 
    return tuple( [ multiindex.get_level_values(i)[column_position] for i in range( len(multiindex.levels) )])    

def multiindex_colum_values(df, top_column_name):
    """
        get the values of a multiindex data frame for a given top_column name
    """
    # slice based on the top column name
    d = df.iloc[:, df.columns.get_level_values(0)==top_column_name]
    # take the first (and the only) column as pd.Series
    try:
        return d[d.columns[0]]
    except:
        raise Exception(f"Could not access the {top_column_name} column")

def parse_qname(qname):
    """
        give a qualified name such as skos:prefLabel (or skos:prefLabel@en with linguistic annotation) 
    """
    p = re.compile(r"""([\w]+){0,1}:([\w\-_]+){1,1}(?:@){0,1}([\w]+){0,1}""")
    try:
        dummy1, prefix, name, language, dummy2 = p.split(qname)
    except:
        raise Exception(f"Could not segment the qualified name: {qname}")
    return  "" if prefix is None else prefix, name, language

def qname_uri(qname, namespaces):
    """
        return the URI for this qname provided that the prefix is found in the list of namescapce tuples 
    """
    prefix, name, language = parse_qname(qname)
    try:
        base = [ ns for ns in namespaces if ns[0] == prefix][0][1] 
    except:
        raise Exception(f"Invalid or unknown qualified name: {qname}")  
    return base+name        

def qname_lang(qname):
    """
        return the language of this qname provided that the prefix is found in the list of namescapce tuples 
    """
    return parse_qname(qname)[2]

# s = "skos:prefLabel@en"
# ss = "skos:prefLabel"
# ss1 = "skossgfd hgfc hghd"

# p = re.compile(r"""([\w]+){1,1}:([\w\-_]+){1,1}(?:@){0,1}([\w]+){0,1}""")
# display(p.split(s))
# display( [ ns for ns in lam_graph.namespaces() if ns[0] == "skos"  ] )
# t = rdf.term.URIRef('http://www.w3.org/2004/02/skos/core#')
# display(t+"/dfdf")

# print ([ ns for ns in lam_graph.namespaces() if ns[0] == ""])
# print (list(lam_graph.namespaces()))

# for s in [":base_local","skos:prefLabel@en","lam:qwe",] :
#     print(parse_qname(s))
#     print(qname_uri(s,lam_graph.namespaces()))
#     print(qname_lang(s,lam_graph.namespaces()))