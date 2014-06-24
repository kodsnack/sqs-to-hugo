#!/usr/bin/python
# vim: set fileencoding=utf-8

from lxml import etree as e
import os, sys
from BeautifulSoup import BeautifulSoup, NavigableString

namespaces = {"content": "http://purl.org/rss/1.0/modules/content/"}

tree = e.parse("squarespace-wordpress-export-06-24-2014.xml")
root = tree.getroot()
try:
    os.mkdir("avsnitt")
except:
    pass
for x in root.findall("./channel/item"):
  title = x.find("title").text
  if title.startswith("attachment-"):
    continue
  title = title.encode("utf-8")

  date = x.find("pubDate").text
  alias = x.find("link").text
  if x.find("status"):
    is_draft = x.find("status").text == "draft"
  else:
    is_draft = False

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
        try:
          links.append((l.a.contents[0], l.a.get("href")))
        except:
          continue
    elif i.contents:
      contentstr += unicode(i.contents[0]) + u"\n"

    try:
      slug = str(int(title.split(" ")[1]))
    except:
      slug = title.replace(" ", "_")

  while os.path.exists("avsnitt/%s.md" % (slug)):
    slug += "_"

  outf = open("avsnitt/%s.md" % (slug), "w")

  outf.write("+++\n")
  outf.write("draft = %s\n" % ("true" if is_draft else "false"))
  outf.write("title = \"" + title + "\"\n")
  outf.write("slug = \"" + str(slug) + "\"\n")
  outf.write("aliases = [\"" + alias + "\"]\n")
  outf.write("categories = [\"avsnitt\"]\n")
  outf.write("+++\n\n")
  outf.write(contentstr.encode("utf-8"))
  outf.write("\n\n")
  outf.write("## Länkar\n---\n")

  for l in links:
    outf.write("* [%s](%s)\n" % (l[0].encode("utf-8"), l[1].encode("utf-8")))

  outf.close()
