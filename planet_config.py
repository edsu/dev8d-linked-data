#!/usr/bin/env python

"""
Queries the triplestore for dev8d people and their blogs and writes out a 
Venus Planet configuration file.
"""

from socket import setdefaulttimeout
from urllib import urlopen

from rdflib.graph import ConjunctiveGraph
from rdflib.namespace import Namespace
from BeautifulSoup import BeautifulSoup

setdefaulttimeout(10)
w = Namespace('http://wiki.2010.dev8d.org/w/Special:URIResolver/Property-3A')

def discover_feed(url):
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html)
        for link in soup.findAll('link', attrs={'rel': 'alternate'}):
            return link['href']
    except Exception, e: 
        pass

def blogs():
    g = ConjunctiveGraph('Sleepycat')
    g.open('store')
    for person, blog in g.subject_objects(predicate=w.Blog):
        name = g.value(subject=person, predicate=w.Name)
        feed_url = discover_feed(blog)
        yield name, feed_url
    g.close()

def print_config():
    print \
"""
[Planet]

name            = dev8d
link            = http://inkdroid.org/dev8d 
owner_name      = Ed Summers
owner_email     = ehs@pobox.com
output_theme    = theme
cache_directory = cache
output_dir      = output
feed_timeout    = 20
items_per_page  = 60
log_level       = DEBUG

# Subscription configuration

"""
    for name, feed in blogs():
        if name and feed:
            print "[%s]\nname = %s\n\n" % (feed, name)

if __name__ == '__main__':
    print_config()
