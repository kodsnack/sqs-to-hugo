#!/usr/bin/python

import xml.etree.ElementTree as e
import os, sys
from BeautifulSoup import BeautifulSoup, NavigableString

namespaces = {"content": "http://purl.org/rss/1.0/modules/content/"}

tree = e.parse("squarespace-wordpress-export-06-24-2014.xml")
root = tree.getroot()
for x in root.findall("./channel/item"):
  title = x.find("title").text
  if title.startswith("attachment-"):
    continue
  print title.encode("utf-8")

  date = x.find("pubDate").text
  alias = x.find("link").text

  content = x.find("content:encoded", namespaces=namespaces).text
  soup = BeautifulSoup(content)

  links = []
  contentstr = u""

  for i in soup:
    if isinstance(i, NavigableString):
      continue
    if i.name == "ul":
      for l in i:
        if isinstance(l, NavigableString):
          continue
        links.append((l.a.contents[0], l.a.get("href")))
    else:
      contentstr += i.contents[0] + "\n"

    try:
      slug = int(title.split(" ")[1])
    except:
      slug = title.replace(" ", "_")

  print "+++"
  print "draft = false"
  print "title = \"" + title + "\""
  print "slug = \"" + str(slug) + "\""
  print "aliases = [\"" + alias + "\"]"
  print "categories = [\"avsnitt\"]"
  print "+++"
  print ""
  print contentstr.encode("utf-8")
  print ""
  print "Laenkar\n--"

  for l in links:
    print "* [%s](%s)" % (l[0].encode("utf-8"), l[1].encode("utf-8"))

  sys.exit(0)
