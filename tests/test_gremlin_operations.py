"""
gremlin_operations
Date: 18.10.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import unittest
import logging
import pathlib

import rdf2g
import rdflib
from pprint import pprint
from gremlin_python.process.graph_traversal import __

LAM_PROPERTY_EXAMPLE = pathlib.Path("../output/lam_project_properties_v2.ttl").resolve()
LAM_CLASS_EXAMPLE = pathlib.Path("../output/lam_project_classes_v2.ttl").resolve()


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.g = rdf2g.setup_graph()

    def test_load_properties(self):
        self.rdf_graph_props = rdflib.Graph()
        self.rdf_graph_props.parse(str(LAM_PROPERTY_EXAMPLE), format="ttl")
        logging.info('%s triples loaded into RDF graph' % str(len(self.rdf_graph_props)))

        rdf2g.clear_graph(self.g)
        assert rdf2g.load_rdf2g(self.g, self.rdf_graph_props), "Could not load the graph"

    # def test_load_classes(self):
    #     self.rdf_graph_classes = rdflib.Graph()
    #     self.rdf_graph_classes.parse(str(LAM_CLASS_EXAMPLE), format="ttl")
    #     logging.info('%s triples loaded into RDF graph' % str(len(self.rdf_graph_classes)))
    #
    #     rdf2g.clear_graph(self.g)
    #     assert rdf2g.load_rdf2g(self.g, self.rdf_graph_classes), "Could not load the graph"

    def test_get_n_levels_down(self):
        known_label = "celexd:md_DTN"
        node = rdf2g.get_node(self.g, known_label)
        tree = rdf2g.generate_traversal_tree(self.g, node, max_depth=1)
        pprint(tree)


if __name__ == '__main__':
    unittest.main()
