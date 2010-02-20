#!/bin/sh

cd /home/ed/Projects/dev8d-linked-data

# refresh dev8d triple store
./crawl.py

# dump rdf for the triple store
./dump.py > /var/www/inkdroid.org/dev8d/dump.rdf

# dump out foafy social graph
./dump_foaf.py > /var/www/inkdroid.org/dev8d/foaf.rdf

# generate dev8d planet config, and move into place atomically 
./planet_config.py > planet/planet.ini.tmp
mv planet/planet.ini.tmp planet/planet.ini

# generate avatars html
./avatars.py > /var/www/inkdroid.org/dev8d/avatars/index.html

# update the dev8d twitter list
./twitter_list.py
