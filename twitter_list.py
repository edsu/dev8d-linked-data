#!/usr/bin/env python

"""
This script will populate a twitter list with dev8d attendees.  You'll need 
oauth2 installed. You'll also need to have run crawl.py to populate the triple 
store. 

The first time you run this script you will be asked what eusername to add the 
dev8d list under, and various other OAuth particulars. You'll need to visit 
https://twitter.com/apps login, create a new application, and note down the 
Consumer key and Consumer secret, which you will be promted to enter.
"""

import urllib
import logging
import os.path
import urlparse
import simplejson

import oauth2 as oauth

from rdflib.namespace import Namespace
from rdflib.graph import ConjunctiveGraph

w = Namespace("http://wiki.2010.dev8d.org/w/Special:URIResolver/Property-3A")

def update_list():
    """
    Reads the triple store looking for twitter usernames and adds 
    them to the dev8d list.
    """
    g = ConjunctiveGraph("Sleepycat")
    g.open("store")

    # get oauth client in order
    credentials = get_credentials()
    consumer = oauth.Consumer(credentials['key'], credentials['secret'])
    client = oauth.Client(consumer, credentials['access_token'])
    list_update_url = 'http://api.twitter.com/1/%s/%s/members.json' % \
        (credentials['list_owner'], credentials['list_name'])

    # create the list if necessary
    create_list(credentials['list_owner'], credentials['list_name'], client)

    # look at all the twitter usernames and add them to the list
    for twitter_username in g.objects(predicate=w['Twitter']):
        id = twitter_user_id(twitter_username, client)
        if id:
            logging.info("adding %s (%s) to list" % (twitter_username, id))
            body = "id=%s" % id
            resp, content = client.request(list_update_url, 'POST', body=body)
        else:
            logging.error("unable to get twitter id for %s" % twitter_username)
    g.close()

def create_list(username, list_name, client):
    list_create_url = 'http://api.twitter.com/1/%s/lists.json' % username
    body = "name=%s"
    client.request(list_create_url, 'POST', body=body)

def twitter_user_id(username, client):
    """
    Return a numeric twitter user id for a given twitter screen name
    """
    url = 'http://api.twitter.com/1/users/show.json?screen_name=%s' % username
    resp, content = client.request(url)
    json = simplejson.loads(content)
    if json.has_key('id'):
        return json['id']
    return None

# complex oauth stuff follows :-)
# this code was basically pulled from the 3-legged example in the 
# documentation at: http://github.com/simplegeo/python-oauth2

def get_credentials():
    credentials = get_stored_credentials()
    if credentials:
        return credentials

    # command line driven authorization, which runs the first time you
    # run this script, after which access_tokens and keys are stored in a config

    list_owner = raw_input('twitter username to own list: ')
    list_name = raw_input('name of the list: ')
    key = raw_input('twitter key: ')
    secret = raw_input('secret: ')
    request_token_url = "http://twitter.com/oauth/request_token"
    access_token_url = "http://twitter.com/oauth/access_token"
    authorize_url = "http://twitter.com/oauth/authorize"

    consumer = oauth.Consumer(key=key, secret=secret)
    client = oauth.Client(consumer, None)
    signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

    resp, content = client.request(request_token_url, "GET")
    request_token = dict(urlparse.parse_qsl(content))

    print "Go to %s?oauth_token=%s in your browser" % \
          (authorize_url, request_token["oauth_token"])
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
    oauth_verifier = raw_input("What is the PIN? ")

    token = oauth.Token(request_token['oauth_token'], 
            request_token['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    resp, content = client.request(access_token_url, "POST", 
            body="oauth_verifier=%s" % oauth_verifier)
    access_token = dict(urlparse.parse_qsl(content))

    token = oauth.Token(access_token['oauth_token'], 
            access_token['oauth_token_secret'])

    save_credentials(list_owner, list_name, key, secret, token)

    return dict(list_owner=list_owner, list_name=list_name, key=key, 
                secret=secret, access_token=token)

def get_stored_credentials():
    config_file = os.path.expanduser('~/.dev8d-twitter')
    if os.path.isfile(config_file):
        try:
            config = open(config_file).read().strip()
            list_owner, list_name, key, secret, token_key, token_secret = config.split(':')
            access_token = oauth.Token(token_key, token_secret)
            return dict(list_owner=list_owner, list_name=list_name, key=key, 
                    secret=secret, access_token=access_token)
        except Exception, e:
            logging.error(e)
            pass
    return None

def save_credentials(list_owner, list_name, key, secret, access_token):
    config = "%s:%s:%s:%s:%s:%s" % (list_owner, list_name, key, secret, 
            access_token.key, access_token.secret)
    config_file = os.path.expanduser('~/.dev8d-twitter')
    open(config_file, 'w').write(config)

if __name__ == '__main__':
    logging.basicConfig(filename="dev8d.log",
                        level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    update_list()
