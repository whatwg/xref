#!/usr/bin/python
import urllib2
try:
    import json
except ImportError:
    import simplejson as json

multipageData = json.loads(urllib2.urlopen("https://html.spec.whatwg.org/multipage/fragment-links.json").read())

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

# Anolis depends on this for some reason
handle = open("w3c-html-generated.json", "w")
handle.write(json.dumps(localData, sort_keys=True, allow_nan=False, indent=2, separators=(',', ': ')))
handle.write("\n")
