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
  audiofile = None

  for i in soup:
    if isinstance(i, NavigableString):
      contentstr += "\n"
      continue

    if i.name == "ul":
      for l in i:
        if isinstance(l, NavigableString):
          continue
        links.append((l.a.contents[0], l.a.get("href")))
    elif i.name == "p":
      for e in i:
        if isinstance(e, NavigableString):
          contentstr += e.string
        elif e.name == "a":
          contentstr += "[%s](%s)" % (e.contents[0], e.get("href"))
      contentstr += "\n"
    elif i.name == "h2":
      contentstr += "## %s ##" % i.string
    elif i.name == "div" and i.get("class") == "sqs-audio-embed":
      audiofile = i.get("data-url")

    try:
      slug = int(title.split(" ")[1])
    except:
      slug = title.replace(" ", "_")

  print "+++"
  print "date = " + date
  print "draft = false"
  print "title = \"" + title + "\""
  print "slug = \"" + str(slug) + "\""
  print "aliases = [\"" + alias + "\"]"
  print "categories = [\"avsnitt\"]"
  if audiofile is not None:
    print "audiofile = \"" + audiofile + "\""
  print "+++"
  print ""
  print contentstr.encode("utf-8")

  for l in links:
    print "* [%s](%s)" % (l[0].encode("utf-8"), l[1].encode("utf-8"))

  sys.exit(0)
