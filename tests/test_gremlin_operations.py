"""
gremlin_operations
Date: 18.10.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import unittest
import logging
from pprint import pprint

import rdf2g
import rdflib
import lam4vb3
from gremlin_python.process.graph_traversal import __
from gremlin_python.structure.graph import Vertex

LAM_PROPERTY_EXAMPLE = lam4vb3.LAM_PROPERTIES_TTL
LAM_CLASS_EXAMPLE = lam4vb3.LAM_CLASSES_TTL


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.g = rdf2g.setup_graph()

    def test_load_properties(self):
        self.rdf_graph_props = rdflib.Graph()
        self.rdf_graph_props.parse(str(LAM_PROPERTY_EXAMPLE), format="ttl")
        logging.info('%s triples loaded into RDF graph' % str(len(self.rdf_graph_props)))

        rdf2g.clear_graph(self.g)
        known_label = "lamd:md_DTN"
        assert rdf2g.load_rdf2g(self.g, self.rdf_graph_props), "Could not load the graph"
        assert rdf2g.get_node(self.g, known_label), "Could not find the node " + known_label

        # def test_load_classes(self):

    #     self.rdf_graph_classes = rdflib.Graph()
    #     self.rdf_graph_classes.parse(str(LAM_CLASS_EXAMPLE), format="ttl")
    #     logging.info('%s triples loaded into RDF graph' % str(len(self.rdf_graph_classes)))
    #
    #     rdf2g.clear_graph(self.g)
    #     assert rdf2g.load_rdf2g(self.g, self.rdf_graph_classes), "Could not load the graph"

    def test_get_n_levels_down(self):
        known_label = "lamd:md_DTN"
        node = rdf2g.get_node(self.g, known_label)
        tree = rdf2g.generate_traversal_tree(self.g, node, max_depth=2)
        exp_tree = rdf2g.expand_tree(self.g, tree)
        assert exp_tree[0]["@label"] == "lamd:md_DTN", "Not the expected node: " + known_label
        assert exp_tree[0]["rdf:type"]["@label"] == "skos:Concept", "Not a concept"

    def test_get_top_collections(self):
        """
            This test works with Version LAM_metadata_05_ECO of the source file
        :return:
        """
        known_label = "skos:Collection"
        type_id = rdf2g.get_node(self.g, known_label)
        # 17 expoected
        collections = self.g.V().as_("node").where(__.out("rdf:type").hasId(type_id.id)).select("node").dedup().toList()
        assert len(collections) == 18, "Did not retrieve the expected  17 collections"
        collections = self.g.V().match(__.as_("a").out("rdf:type").hasId(type_id.id),
                                       __.as_("a").in_("skos:member")).select("a").properties(
            "skos:prefLabel").toList()
        assert len(collections) == 9, "Did not retrieve the expected 9 collections"

        collections = self.g.V().match(__.as_("a").out("rdf:type").hasId(type_id.id),
                                       __.not_(__.as_("a").in_("skos:member"))).select("a").toList()
        assert len(collections) == 9, "Did not retrieve the expected 8 collections"


if __name__ == '__main__':
    unittest.main()
