#!/usr/bin/env python

import re
import urllib
import logging

from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef
from rdflib.namespace import Namespace

w = Namespace('http://wiki.2010.dev8d.org/w/Special:URIResolver/Property-3A')
owl = Namespace('http://www.w3.org/2002/07/owl#')

def fetch(graph, url):
    logging.debug("removing context for %s" % url)
    for t in graph.get_context(url):
        graph.remove(t)
    logging.debug("parsing %s" % url)
    try:
        graph.parse(url)
    except Exception, e:
        logging.error(e)

def users():
    html = urllib.urlopen('http://wiki.2010.dev8d.org/w/Category:Person').read()
    for user in re.findall(r'"/w/User:(\w+)"', html):
        yield user

def fetch_users(graph):
    for user in users():
        url = 'http://wiki.2010.dev8d.org/w/Special:ExportRDF/User:%s' % user
        logging.info('fetching info for user: %s' % user)
        fetch(graph, url)

def fetch_programme(graph):
    url = 'http://data.dev8d.org/2010/programme/dev8d_programme.rdf'
    logging.info("fetching programme")
    fetch(graph, url)

def fetch_affiliations(graph):
    seen = set()
    for affiliate in graph.objects(predicate=w['Affiliation']):
        if affiliate not in seen:
            logging.info("fetching info for affiliate %s" % affiliate)
            fetch(graph, affiliate)
            seen.add(affiliate)

def fetch_twitter(graph):
    seen = set()
    # all the semantictwitter data is thrown into the same graph
    context = URIRef('http://semantictweet.com')
    for user, twitter_user in graph.subject_objects(predicate=w['Twitter']):
        twitter_uri = URIRef('http://semantictweet.com/%s#me' % twitter_user)
        if twitter_uri not in seen:
            logging.info('fetching twitter info for %s' % twitter_user)
            # connect the wiki user with the twitter user
            graph.addN([(user, owl.sameAs, twitter_uri, context)])
            fetch(graph, twitter_uri)
            seen.add(twitter_uri)

if __name__ == '__main__':
    logging.basicConfig(filename="crawl.log", 
                        level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("starting crawl")
    graph = ConjunctiveGraph('Sleepycat')
    graph.open('store', create=True)
    fetch_users(graph)
    fetch_programme(graph)
    fetch_affiliations(graph)
    fetch_twitter(graph)
    graph.close()
    logging.info("finished crawl")
