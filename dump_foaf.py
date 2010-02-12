#!/usr/bin/env python

import sys

import rdflib

FOAF = rdflib.namespace.Namespace('http://xmlns.com/foaf/0.1/')
RDF = rdflib.namespace.RDF

g = rdflib.graph.ConjunctiveGraph("Sleepycat")
g.open('store')

# create a sub-graph of just foafy bits
foaf = rdflib.graph.Graph()
for subject in g.subjects(predicate=RDF.type, object=FOAF.Person):
    for triple in g.triples((subject, None, None)):
        foaf.add(triple)

# save off the foafy bits as rdf/xml
foaf.serialize(sys.stdout)
g.close()

