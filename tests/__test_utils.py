"""
test_utils
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com
"""

import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


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

if __name__ == '__main__':
    unittest.main()
