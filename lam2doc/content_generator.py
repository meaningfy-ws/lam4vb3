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
from lam2doc import CONCEPT_SCHEME_QNAME, CONCEPT_QNAME
from lam2doc.abstract_generator import ContentGenerator


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

    def __generate_tree(self, node_type, default_max_depth=3):
        css = rdf2g.get_nodes_of_type(self.g, node_type)
        css_trees = [rdf2g.generate_traversal_tree(self.g, cs, default_max_depth) for cs in css]
        css_exp_tees = [rdf2g.expand_tree(self.g, cs_tree) for cs_tree in css_trees]
        # flatten the dicts
        css_exp_tees = [i[0] if len(i) == 1 else i for i in css_exp_tees]
        self.content[node_type] = css_exp_tees

    def generate(self, force=False, ):
        if force:
            self.content = None

        if not self.content:
            self.content = {}
            # look for skos:ConceptSchemes
            self.__generate_tree(CONCEPT_SCHEME_QNAME)
            # look for skos:Concept
            self.__generate_tree(CONCEPT_QNAME)
        return self.content

    def sort(self, key, by=None, ascending=True):
        """
            provide json path
        :param key:
        :param by:
        :param ascending:
        :return:
        """
        pass


    def to_json(self, output_file_name):
        with open(str(output_file_name), "w") as json_file:
            json.dump(self.generate(), json_file)

    def to_xml(self, output_file_name):
        with open(str(output_file_name), "wb") as xml_file:
            xml_file.write(dicttoxml.dicttoxml(self.generate(), attr_type=True, cdata=True))

    def serialise(self, output_file):
        self.to_json(output_file)
