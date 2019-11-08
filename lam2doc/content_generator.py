"""
contentGenerator
Date: 27.10.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import dicttoxml
import rdf2g
import json
import rdflib
from lam2doc import CONCEPT_SCHEME_QNAME, CONCEPT_QNAME, COLLECTION_QNAME
from lam2doc.abstract_generator import ContentGenerator
from gremlin_python.process.graph_traversal import __


class LAMGremlinGenerator(ContentGenerator):
    """
        generic class for generating data content using gremlin tree queries on property graphs.
        - connect
        - query
        - reduce query

    """

    def __init__(self, rdf_file, connection_string=rdf2g.DEFAULT_LOCAL_CONNECTION_STRING, ):

        self.content = None

        self.g = rdf2g.setup_graph(connection_string)
        rdf2g.clear_graph(self.g)

        self.rdf_graph = rdflib.Graph()
        self.rdf_graph.parse(str(rdf_file), format=rdflib.util.guess_format(str(rdf_file)))
        rdf2g.clear_graph(self.g)
        rdf2g.load_rdf2g(self.g, self.rdf_graph)
        # self.query_dict = {"skos:ConceptScheme": "skos:ConceptScheme",
        #                    "skos:Concept": "skos:Concept"}

    def __generate_tree(self, for_nodes, content_key, default_max_depth=3):
        css_trees = [rdf2g.generate_traversal_tree(self.g, root_=cs, max_depth=default_max_depth) for cs in for_nodes]
        css_exp_tees = [rdf2g.expand_tree(self.g, cs_tree) for cs_tree in css_trees]
        # flatten the dicts
        css_exp_tees = [i[0] if len(i) == 1 else i for i in css_exp_tees]
        self.content[content_key] = css_exp_tees

    def __generate_tree_by_type(self, node_type, default_max_depth=3):
        css = rdf2g.get_nodes_of_type(self.g, node_type)
        self.__generate_tree(for_nodes=css, content_key=node_type, default_max_depth=default_max_depth)

    def __get_top_collections(self, collection_qname="skos:Collection"):
        """
            get nodes that are collections and have no incoming skos:member relations
        :return:
        """
        type_id = rdf2g.get_node(self.g, collection_qname)
        collections = self.g.V().match(__.as_("a").out("rdf:type").hasId(type_id.id),
                                       __.not_(__.as_("a").in_("skos:member"))).select("a").toList()
        return collections

    def generate(self, force=False, ):
        if force:
            self.content = None

        if not self.content:
            self.content = {}
            # look for skos:ConceptSchemes
            self.__generate_tree_by_type(CONCEPT_SCHEME_QNAME)
            # look for skos:Concept
            self.__generate_tree_by_type(CONCEPT_QNAME)
            # look for skos:Collections
            self.__generate_tree(for_nodes=self.__get_top_collections(),
                                 content_key=COLLECTION_QNAME,
                                 default_max_depth=6)
        return self.content

    def to_json(self, output_file_name):
        with open(str(output_file_name), "w") as json_file:
            json.dump(self.generate(), json_file)

    def to_xml(self, output_file_name):
        with open(str(output_file_name), "wb") as xml_file:
            xml_file.write(dicttoxml.dicttoxml(self.generate(), attr_type=True, cdata=True))

    def serialise(self, output_file):
        self.to_json(output_file)
