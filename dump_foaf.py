#!/usr/bin/env python

import sys
import logging

import rdflib

logging.basicConfig(filename="dev8d.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("starting dump of foaf social graph")

FOAF = rdflib.Namespace('http://xmlns.com/foaf/0.1/')
RDF = rdflib.namespace.RDF

g = rdflib.ConjunctiveGraph("Sleepycat")
g.open('store')

# create a sub-graph of just foafy bits
foaf = rdflib.Graph()
for subject in g.subjects(predicate=RDF.type, object=FOAF.Person):
    for triple in g.triples((subject, None, None)):
        foaf.add(triple)

# save off the foafy bits as rdf/xml
foaf.serialize(sys.stdout)
g.close()

logging.info("finished dump of foaf social graph")

