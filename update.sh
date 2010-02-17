#!/bin/sh

cd /home/ed/Projects/dev8d-linked-data

# regenerate dev8d triple store
./crawl.py

# dump rdf for the triple store
./dump.py > /var/www/inkdroid.org/planet-dev8d/dump.rdf

# dump out foafy social graph
./dump_foaf.py > /var/www/inkdroid.org/planet-dev8d/foaf.rdf

# generate dev8d planet config, and move into place atomically 
./planet_config.py > planet/planet.ini.tmp
mv planet/planet.ini.tmp planet/planet.ini
