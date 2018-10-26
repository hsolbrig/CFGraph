import unittest
from typing import List, Tuple

from rdflib import URIRef, RDF
# <http://a.example/s1>  <http://a.example/p1> "a","b","c","d","e","f" .
from rdflib.term import Literal

from CFGraph import CFGraph

s1 = URIRef("http://a.example/s1")
s2 = URIRef("http://a.example/s2")
s3 = URIRef("http://a.example/s3")
s4 = URIRef("http://a.example/s4")

p = URIRef("http://a.example/p1")

rdf = '<http://a.example/s1> <http://a.example/p1> ("a" "b" "c" "d" "e" "f" "b").'
rdf2 = '<http://a.example/s2> <http://a.example/p1> "a", "b", "c", "d", "e", "f", "b".'
empty = '<http://a.example/s3> <http://a.example/p1> ().'
onemember = '<http://a.example/s4> <http://a.example/p1> ("a").'


class ListTestCase(unittest.TestCase):

    @staticmethod
    def gen_list(subj: URIRef, objs: List[str]) -> List[Tuple[URIRef, URIRef, Literal]]:
        return [(subj, p, Literal(e)) for e in objs]

    @staticmethod
    def gen_lit_list(objs: List[str]) -> List[Literal]:
        return [Literal(o) for o in objs]

    """ Flatten an RDF collection """
    def test_flatten(self):
        g = CFGraph()
        g.parse(data=rdf, format='turtle')
        g.parse(data=rdf2, format='turtle')
        g.parse(data=empty, format='turtle')
        g.parse(data=onemember, format='turtle')
        self.assertEqual(self.gen_list(s1, ["a", "b", "c", "d", "e", "f", "b"]), list(g.triples((s1, p, None))))
        self.assertEqual(self.gen_lit_list(["a", "b", "c", "d", "e", "f", "b"]), list(g.objects(s1, p)))
        self.assertEqual(set(self.gen_lit_list(["a", "b", "c", "d", "e", "f", "b"])), set(g.objects(s2, p)))
        self.assertEqual([], list(g.objects(s3, p)))
        self.assertEqual([Literal("a")], list(g.objects(s4, p)))


if __name__ == '__main__':
    unittest.main()
