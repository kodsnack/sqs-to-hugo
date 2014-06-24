#!/usr/bin/python

import xml.etree.ElementTree as e
import os, sys
from BeautifulSoup import BeautifulSoup, NavigableString
from datetime import datetime

namespaces = {"content": "http://purl.org/rss/1.0/modules/content/"}

tree = e.parse("squarespace-wordpress-export-06-24-2014.xml")
root = tree.getroot()

def getContent(node):
  contentstr = ""
  for n in node:
    if isinstance(n, NavigableString):
      contentstr += n.string
      continue
    elif isinstance(n, unicode):
      contentstr += n
      continue

    if n.name == "ul" or n.name == "p":
      contentstr += getContent(n)
      if n.name == "p":
        contentstr += "\n"
    elif n.name == "h2":
      contentstr += "## %s ##" % n.string
    elif n.name == "a":
      contentstr += "[%s](%s)" % (n.contents[0], n.get("href"))
    elif n.name == "li":
      contentstr += "* " + getContent(n)

  return contentstr

for x in root.findall("./channel/item"):
  title = x.find("title").text
  if title.startswith("attachment-"):
    continue

  # Sun, 02 Sep 2012 18:32:03 +0000
  date = x.find("pubDate").text.replace(" +0000", "")
  pdate = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S")
  # 2012-09-16T09:30:00Z
  date = pdate.strftime("%Y-%m-%dT%H:%M:%SZ")

  alias = x.find("link").text

  content = x.find("content:encoded", namespaces=namespaces).text
  soup = BeautifulSoup(content)

  links = []
  contentstr = getContent(soup)
  audiofile = None
  for d in soup.findAll("div"):
    if d.get("class") == "sqs-audio-embed":
      audiofile = d.get("data-url")

  try:
    slug = int(title.split(" ")[1])
  except:
    slug = float(title.split(" ")[1]) 

  print slug

  fp = open("content/%s.md" % slug, "w")

  fp.write("+++\n")
  fp.write("date = %s\n" % date)
  fp.write("draft = false\n")
  fp.write("title = \"%s\"\n" % title.encode("utf-8"))
  fp.write("slug = \"%s\"\n" % str(slug))
  fp.write("aliases = [\"%s\"]\n" % alias)
  fp.write("categories = [\"avsnitt\"]\n")
  if audiofile is not None:
    fp.write("audiofile = \"%s\"\n" % audiofile)
  fp.write("+++\n")
  fp.write("\n")
  fp.write(contentstr.encode("utf-8"))
  fp.write("\n")
  fp.close()

