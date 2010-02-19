#!/usr/bin/env python

"""
Messy little hack to print out a bunch of twitter avatars for dev8d
attendees that are linked to their twitter profiles.
"""

import rdflib

wiki = rdflib.Namespace("http://wiki.2010.dev8d.org/w/Special:URIResolver/")
foaf = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
owl  = rdflib.Namespace("http://www.w3.org/2002/07/owl#")

def attendee(graph, person):
    for other_uri in graph.subjects(predicate=owl.sameAs, object=person):
        if 'dev8d.org' in other_uri:
            return True
    return False

def people(graph):
    for person, avatar in graph.subject_objects(predicate=foaf.img):
        if not attendee(graph, person):
            continue
        name = graph.value(subject=person, predicate=foaf.name)
        nick = graph.value(subject=person, predicate=foaf.nick)
        twitter = 'http://twitter.com/%s' % nick 
        yield person, name, twitter, avatar

def print_avatars_html(graph):
    print \
"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.0//EN" "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd"> 

<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:foaf="http://xmlns.com/foaf/0.1/">
    <head>
        <title>dev8d attendees</title>
        <style type="text/css">
           body {
             font-family: Verdana; 
             margin-left: 7%;
             margin-right: 7%;
           }
        </style>
    </head>
    <body>
        <div style="text-align: center;">
            <h1>dev8d attendees</h1>
            <a href="http://www.w3.org/2007/08/pyRdfa/extract?format=turtle&amp;uri=http://inkdroid.org/planet-dev8d/avatars">
                <img src="http://www.w3.org/Icons/SW/Buttons/sw-rdfa-gray.png" />
            </a>
        </div>
        <br />
        <div id="avatars">
"""
    for person, name, twitter, avatar in people(graph):
        chunk = \
"""
<span about="%s" typeof="foaf:Person">
    <a rel="foaf:homepage" href="%s">
        <img resource="%s" rev="foaf:img" title="%s" 
             alt="%s" width="80" src="%s" />
    </a>
</span>
""" % (person, twitter, person, name, name, avatar)
        print chunk.encode('utf-8')

    print "</div>\n</body>\n</html>"

if __name__ == '__main__':
    graph = rdflib.ConjunctiveGraph('Sleepycat')
    graph.open('store')
    print_avatars_html(graph)
    graph.close()
