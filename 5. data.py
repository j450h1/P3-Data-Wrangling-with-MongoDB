# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 16:10:45 2015

@author: user
"""
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. You could also do some cleaning
before doing that, like in the previous exercise, but for this exercise you just have to
shape the structure.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

import os
#Set the proper current working directory
os.getcwd()
os.chdir('C:/Users/user/version-control/Data-Wrangle-OpenStreetMaps-MongoDB')

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

file_in = 'GVRD - Vancouver - OSM XML Raw.osm'
data = list()
for _, element in ET.iterparse(file_in):
    node = {}
    node['pos'] = [float(1),float(1)]
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag  
        for attrName, attrValue in element.attrib.items():
            if attrName == "lat" or attrName == "lon": #pos
                if attrName == "lat":
                    node['pos'][0] = float(attrValue)
                if attrName == "lon":
                    node['pos'][1] = float(attrValue)            
            else:
                 node[attrName] = attrValue
            #2nd level nodes      
            ndtags = element.findall("./*")        
            for ndtag in ndtags:
                
      data.append(node)        
    element.clear()

    



def shape_element(element):
    node = {}
#    node['created'] = {}
    node['pos'] = [float(1),float(1)]
    double_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
    from collections import defaultdict
    node = defaultdict()
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        for attrName, attrValue in element.attrib.items():
            if attrName == "lat" or attrName == "lon": #pos
                if attrName == "lat":
                    node['pos'][0] = float(attrValue)
                if attrName == "lon":
                    node['pos'][1] = float(attrValue)            
            else:
                node[attrName] = attrValue
        #if their is a second level node
        ndtags = element.findall("./*")
        for ndtag in ndtags:
        #   print ndtag.tag
        #   print ndtag.attrib
            kname, kvalue, vname, vvalue, refname, refvalue = ["","","","","",""]
            for aName, aValue in ndtag.attrib.items():
                #print aName, aValue, "1"
                if aName == "k":
                    kname = aName
                    kvalue = aValue
                elif aName == "v":
                    vname = aName
                    vvalue = aValue
                elif aName == "ref":
                    refname = aName
                    refvalue = aValue
            m = double_colon.search(kvalue)
            p = problemchars.search(kvalue)
#if second level tag "k" value contains problematic characters, it should be ignored
            if p is not None:
                continue
# if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
            elif kvalue.startswith("addr:") and 'address' not in node.keys():
                if m is not None: #if there are two colons, ignore the tag                        
                    continue                        
                else:                        
                    node['address'][kvalue.split("addr:")[1]] = vvalue    
            elif kvalue.startswith("addr:") and 'address' in node.keys():
                if m is not None: #if there are two colons, ignore the tag                        
                    continue                        
                else:                        
                    node['address'][kvalue.split("addr:")[1]] = vvalue
# if there is a second ":" that separates the type/direction of a street,
# the tag should be ignored, for example:
            elif not kvalue.startswith("addr:") and m is not None:
                continue
            else:
                if element.tag == "way" and refname == "ref" and "node_refs" not in node.keys():
                    node["node_refs"].append(refvalue)
                elif element.tag == "way" and refname == "ref" and "node_refs" in node.keys():
                    node["node_refs"].append(refvalue)
                else:
                    node[kvalue] = vvalue
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
#                if pretty:
#                    fo.write(json.dumps(el, indent=2)+"\n")
#                else:
#                    fo.write(json.dumps(el) + "\n")
    return data

data = process_map('GVRD - Vancouver - OSM XML Raw.osm', False)
#pprint.pprint(data)

assert data[0] == {
                    "id": "261114295", 
                    "visible": "true", 
                    "type": "node", 
                    "pos": [
                      41.9730791, 
                      -87.6866303
                    ], 
                    "created": {
                      "changeset": "11129782", 
                      "user": "bbmiller", 
                      "version": "7", 
                      "uid": "451048", 
                      "timestamp": "2012-03-28T18:31:23Z"
                    }
                  }
assert data[-1]["address"] == {
                                "street": "West Lexington St.", 
                                "housenumber": "1412"
                                  }
assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
                                "2199822370", "2199822284", "2199822281"]

