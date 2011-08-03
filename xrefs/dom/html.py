import urllib2
import json

# HAHAHA HACK (Reads out the first line and makes it parseable as JSON)
multipageData = json.loads(urllib2.urlopen("http://www.whatwg.org/specs/web-apps/current-work/multipage/fragment-links.js").readline()[21:-1].replace("','", '","').replace("' };", '"}').replace("':'", '":"').replace("\\'", "'").replace("{ '", '{"'))

localData = json.loads(open("html.json", "r").read())

# Updates our local mapping of terms and identifiers with links to the
# multipage version. This will fail if our local mapping is wrong.
for term, identifier in localData["definitions"].items():
    localData["definitions"][term] = multipageData[identifier] + ".html#" + identifier

handle = open("html-generated.json", "w")
handle.write(json.dumps(localData))
