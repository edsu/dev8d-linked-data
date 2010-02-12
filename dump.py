#!/usr/bin/env python

import sys

from rdflib.graph import ConjunctiveGraph

g = ConjunctiveGraph("Sleepycat")
g.open('store')
g.serialize(sys.stdout)
g.close()

