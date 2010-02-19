#!/usr/bin/env python

import rdflib

wiki = rdflib.Namespace("http://wiki.2010.dev8d.org/w/Special:URIResolver/")
foaf = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
owl  = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
conf = rdflib.URIRef("")

def attendee(graph, person):
    for other_uri in graph.subjects(predicate=owl.sameAs, object=person):
        if 'dev8d.org' in other_uri:
            return True
    return False

def people(graph):
    for person, avatar in graph.subject_objects(predicate=foaf.img):
        if not attendee(graph, person):
            continue
        homepage = graph.value(subject=person, predicate=foaf.homepage)
        name = graph.value(subject=person, predicate=foaf.name)
        yield name, homepage, avatar

def print_avatars_html(graph):
    print "<html>\n<head>\n<body>\n<table>\n<tr>\n"
    count = 0
    for name, homepage, avatar in people(graph):
        count += 1
        if count % 15 == 0:
            print "</tr>\n<tr>\n"
        td = \
"""
<td>
    <a href="%s">
        <img title="%s" width="80" src="%s">
    </a>
</td>
""" % (homepage, name, avatar)
        print td.encode('utf-8')
    print "</tr>\n</table>\n</body>\n</html>"

if __name__ == '__main__':
    graph = rdflib.ConjunctiveGraph('Sleepycat')
    graph.open('store')
    print_avatars_html(graph)
    graph.close()
