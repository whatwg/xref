#!/usr/bin/python
import urllib2
try:
    import json
except ImportError:
    import simplejson as json

# HAHAHA HACK (Reads out the first line)

to = - (len(",};var fragid = window.location.hash.substr(1);if ((!fragid) || !(fragid in fragment_links)) {var m = window.location.pathname.match(/\/(?:section-)?([\w\-]+)\.html/);if (m) fragid = m[1];}var page = fragment_links[fragid];if (page) {window.location.replace(page+'.html#'+fragid);}") + 1)

multipageData = json.loads(urllib2.urlopen("https://html.spec.whatwg.org/multipage/fragment-links.js").readline()[21:to] + "}")

localData = json.loads(open("html.json", "r").read())

# Updates our local mapping of terms and identifiers with links to the
# multipage version. This will fail if our local mapping is wrong.
errors = []
for term, identifier in localData["definitions"].items():
    if identifier not in multipageData:
        errors.append(identifier)
        continue
    localData["definitions"][term] = multipageData[identifier] + ".html#" + identifier

if errors:
    raise Exception, errors

handle = open("html-generated.json", "w")
handle.write(json.dumps(localData, sort_keys=True, allow_nan=False, indent=2, separators=(',', ': ')))
handle.write("\n")

# Write a copy for W3C HTML
localData["url"] = "http://www.w3.org/html/wg/drafts/html/master/"

handle = open("w3c-html-generated.json", "w")
handle.write(json.dumps(localData, sort_keys=True, allow_nan=False, indent=2, separators=(',', ': ')))
handle.write("\n")
