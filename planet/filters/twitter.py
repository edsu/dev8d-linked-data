#!/usr/bin/env python

"""
Remove redundant content element from twitter feed.
"""

import sys

from xml.etree import ElementTree as et

entry = et.parse(sys.stdin).getroot()

id = entry.find('id')
if id and 'tag:twitter.com' in id.text:
    content = entry.find('content')
    entry.remove(content)

print et.tostring(entry, 'utf-8')
