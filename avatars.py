#!/usr/bin/env python

"""
Messy little hack to print a bunch of twitter avatars for dev8d
attendees as rdfa xhtml using the triples that are crawled from
semantic media wiki and elsewhere.
"""

import rdflib

wiki = rdflib.Namespace("http://wiki.2010.dev8d.org/w/Special:URIResolver/")
foaf = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
owl  = rdflib.Namespace("http://www.w3.org/2002/07/owl#")

def attendee(graph, person):
    """
    A hack to use owl:sameAs assertions created during crawling 
    to determine if a given user on semantictweet is a dev8d attendee
    """
    for other_uri in graph.subjects(predicate=owl.sameAs, object=person):
        if 'dev8d.org' in other_uri:
            return other_uri
    return False

def people(graph):
    for person, avatar in graph.subject_objects(predicate=foaf.img):
        dev8d_uri = attendee(graph, person)
        if not dev8d_uri:
            continue

        name = graph.value(subject=person, predicate=foaf.name)
        nick = graph.value(subject=person, predicate=foaf.nick)
        twitter = 'http://twitter.com/%s' % nick 
        yield dev8d_uri, person, name, twitter, avatar

def print_avatars_html(graph):
    print \
"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.0//EN" "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd"> 

<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:foaf="http://xmlns.com/foaf/0.1/"
      xmlns:owl="http://www.w3.org/2002/07/owl#">
    <head>
        <title>dev8d attendees</title>
        <style type="text/css">
           body {
             text-align: center;
             font-family: Verdana; 
             margin-left: 7%;
             margin-right: 7%;
           }
           #about {
             margin: 0px auto;
             border: thin solid gray;
             background-color: #ccffcc;
             width: 60%;
             padding: 10px;
           }
        </style>
    </head>
    <body>
        <div id="banner">
            <h1><a href="http://dev8d.org">dev8d</a> attendees on 
            <a href="http://twitter.com/edsu/dev8d">twitter</a></h1>
            <a href="http://www.w3.org/2007/08/pyRdfa/extract?format=turtle&amp;uri=http://inkdroid.org/planet-dev8d/avatars/">
                <img alt="rdfa" title="get turtle for this page" src="http://www.w3.org/Icons/SW/Buttons/sw-rdfa-gray.png" />
            </a>
            <br />
            <br />
        </div>
        <div id="avatars">
"""
    for dev8d_uri, person, name, twitter, avatar in people(graph):
        chunk = \
"""
<span about="%s" typeof="foaf:Person">
    <a rel="foaf:homepage" href="%s">
        <img resource="%s" rev="foaf:img" title="%s" 
             alt="%s" width="80" src="%s" />
    </a>
    <span rel="owl:sameAs" resource="%s"></span>
</span>
""" % (person, twitter, person, name, name, avatar, dev8d_uri)
        print chunk.encode('utf-8')

    print \
"""
        <br />
        <br />
        </div>
        <p id="about">
        This page is <a
        href="http://github.com/edsu/dev8d-linked-data/blob/master/avatars.py">regenerated</a>
        every two hours based on information stored in the <a
        href="http://wiki.dev8d.org">dev8d semantic media wiki</a>
        and social graph information in 
        <a href="http://semantictweet.com">semantictweeet</a>. 
        If you want to show up here add your twitter id to your 
        user profile, see <a href="http://wiki.2010.dev8d.org/w/User:Dfflanders">dfflanders</a> 
        profile for an example.
        <br />
        </p>
    </body>
</html>
"""
 
if __name__ == '__main__':
    graph = rdflib.ConjunctiveGraph('Sleepycat')
    graph.open('store')
    print_avatars_html(graph)
    graph.close()
