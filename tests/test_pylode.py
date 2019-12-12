"""
test_pylode.py
Date: 02/11/2019
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com 
"""

import unittest

import pylode
import rdflib

from lam2doc import LAM_OWL_TTL, LAM_OWL_HTML


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.rdf_graph = rdflib.Graph()
        self.rdf_graph.parse(str(LAM_OWL_TTL), format="ttl")

    @unittest.skip("PyLode is not so interesting for the moment")
    def test_running_pylode(self):
        h = pylode.MakeHtml()
        h.G = self.rdf_graph
        source_info = (str(LAM_OWL_TTL), "ttl")
        # generate the HTML doc
        with LAM_OWL_HTML.open('w') as f:
            f.write(h.generate_html(str(source_info)))


if __name__ == '__main__':
    unittest.main()
