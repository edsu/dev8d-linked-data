#!/usr/bin/env python

import sys
import logging

import rdflib

logging.basicConfig(filename="dev8d.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("started dumping store as rdf/xml")
g = rdflib.ConjunctiveGraph("Sleepycat")
g.open('store')
g.serialize(sys.stdout)
g.close()
logging.info("finished dumping store as rdf/xml")

