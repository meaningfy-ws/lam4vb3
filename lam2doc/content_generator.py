"""
contentGenerator
Date: 18.10.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

from abc import ABC, abstractmethod
import rdf2g
import logging
import pathlib
import json

import rdflib

CONCEPT_SCHEME_QNAME = "skos:ConceptScheme"
CONCEPT_QNAME = "skos:Concept"


class ContentGenerator(ABC):
    """
    generic data content generator
    """

    @abstractmethod
    def generate(self):
        """
        Generates the data content object from a data source
        :return: dict
        """


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

    def generate(self, force=False):
        if force:
            self.content = None

        if not self.content:
            self.content = {}

            # look for skos:ConceptSchemes
            css = rdf2g.get_nodes_of_type(self.g, CONCEPT_SCHEME_QNAME)
            css_trees = [rdf2g.generate_traversal_tree(self.g, cs, 1) for cs in css]
            css_exp_tees = [rdf2g.expand_tree(self.g, cs_tree) for cs_tree in css_trees]
            # flatten the dicts
            css_exp_tees = [i[0] if len(i) > 1 else i for i in css_exp_tees]
            self.content[CONCEPT_SCHEME_QNAME] = css_exp_tees

            # look for skos:ConceptSchemes
            cs = rdf2g.get_nodes_of_type(self.g, CONCEPT_QNAME)
            cs_trees = [rdf2g.generate_traversal_tree(self.g, c) for c in cs]
            cs_exp_tees = [rdf2g.expand_tree(self.g, c_tree) for c_tree in cs_trees]
            cs_exp_tees = [i[0] if len(i) > 1 else i for i in cs_exp_tees]
            self.content[CONCEPT_QNAME] = cs_exp_tees

        return self.content

    def to_json(self, output_file_name):
        if not self.content:
            self.generate()

        with open(output_file_name, "w") as json_file:
            json.dump(self.content, json_file)
