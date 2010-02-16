#!/usr/bin/env python

"""
Queries the triplestore for dev8d people and their blogs, figures out the 
feed url for the blog and writes out a Planet Venus configuration file.
"""

from socket import setdefaulttimeout
from urllib import urlopen
from urlparse import urlparse

import logging

from rdflib.graph import ConjunctiveGraph
from rdflib.namespace import Namespace
from BeautifulSoup import BeautifulSoup

import feedparser

setdefaulttimeout(10)
w = Namespace('http://wiki.2010.dev8d.org/w/Special:URIResolver/Property-3A')

def discover_feed(url):
    logging.info("looking up feed url for %s" % url)
    feed_url = None
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html)
        for link in soup.findAll('link', attrs={'rel': 'alternate'}):
            feed_url = link['href']
            # rewrite to feed to be absolute if its relative
            if feed_url and not feed_url.startswith('http'):
                u = urlparse(url)
                feed_url = 'http://%s%s' % (u.netloc, feed_url)
            # check that the feed is there and looks ok
            if feed_ok(feed_url):
                break
    except Exception, e: 
        logging.error("error when performing feed discovery for %s: %s" % 
                      (url, e))
    return feed_url

def feed_ok(url):
    logging.info("checking feed: %s" % url)
    try:
        feed = feedparser.parse(url)
        if len(feed.entries) > 0 and not hasattr(feed.entries[0], 'updated'):
            logging.error("feed %s has entries without updated timestamp" % url)
            return False
    except Exception, e:
        logging.error("error when checking feed %s: %s" % (url, e))
        return False
    return True


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

name            = planet-dev8d
link            = http://inkdroid.org/planet-dev8d
owner_name      = Ed Summers
owner_email     = ehs@pobox.com
output_theme    = theme
cache_directory = cache
output_dir      = /var/www/inkdroid.org/planet-dev8d
feed_timeout    = 20
items_per_page  = 60
log_level       = DEBUG

# Subscription configuration

"""
    for name, feed in blogs():
        if name and feed:
            print "[%s]\nname = %s\n\n" % (feed, name)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("generating planet config")
    print_config()
    logging.info("finished generating planet config")
