#!/usr/bin/env python

import sys
import logging

from rdflib.graph import ConjunctiveGraph

logging.basicConfig(filename="dev8d.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("started dumping store as rdf/xml")
g = ConjunctiveGraph("Sleepycat")
g.open('store')
g.serialize(sys.stdout)
g.close()
logging.info("finished dumping store as rdf/xml")

