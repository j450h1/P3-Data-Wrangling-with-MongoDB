# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 16:10:45 2015

@author: user
"""
import xml.etree.ElementTree as ET
import re
import codecs
import json

"""
You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. You could also do some cleaning
before doing that, like in the previous exercise, but for this exercise you just have to
shape the structure.
"""
import os
#Set the proper current working directory
os.getcwd()
os.chdir('C:/Users/user/version-control/Project-2-Data-Wrangling-with-MongoDB')
#Problem character searches for the 2 problem values we found in audit 
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
#double_colon searches - example addr: street:
double_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
#the street type ending, example street, st., road
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) 
#needed to check if lower_colon in name
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
#skip,changes, and mapping retrieved from looking at the results of audit.py
skip = ["10","32500","99","Tsawwassen","Park","Terminal","8500"]
changes = { 'ing George Hwy.': 'King George Boulevard',
           'W15th st': 'W 15th Street',
           'Howe St. Vancouver': 'Howe Street',
           'W. Hastings St. Vancouver': 'West Hastings Street',
           'Expo Blvd, #3305': 'Expo Boulevard',            
           ' Beatty St': 'Beatty Street'} 
mapping = {'10': '10',
           '3305': '3305',
           '32500': '32500',
           '77A': '77A Avenue',
           '8500': '8500',
           '99': '99',
           'Alley': 'Alley',
           'Ave': 'Avenue',
           'Ave.': 'Avenue',
           'Blvd': 'Boulevard',
           'Broadway': 'Broadway',
           'Bypass': 'Bypass',
           'Centre': 'Centre',
           'Close': 'Close',
           'Crescent': 'Crescent',
           'Diversion': 'Diversion',
           'Dr': 'Drive',
           'Dr.': 'Drive',
           'East': 'East',
           'Edmonds': 'Edmonds Street',
           'Gate': 'Gate',
           'Grove': 'Grove',
           'Hastings': 'Hastings Street',
           'Highway': 'Highway',
           'Hwy': 'Highway',
           'Hwy.': 'Highway',
           'Kingsway': 'Kingsway',
           'Mall': 'Mall',
           'Mews': 'Mews',
           'Moncton': 'Moncton Street',
           'North': 'North',
           'Park': 'Park',
           'Pender': 'Pender Street',
           'RD': 'Road',
           'Rd': 'Road',
           'Rd.': 'Road',
           'Road,': 'Road',
           'S.': 'South',
           'Sanders': 'Sanders Street',
           'South': 'South',
           'St': 'Street',
           'St.': 'Street',
           'Street3': 'Street',
           'Terminal': 'Terminal',
           'Tsawwassen': 'North Tsawwassen',
           'Vancouver': 'Vancouver',
           'Walk': 'Walk',
           'Way': 'Way',
           'West': 'West',
           'Willingdon': 'Willingdon',
           'Wynd': 'Wynd',
           'av': 'Avenue',
           'road': 'Road',
           'st': 'Street',
           'street': 'Street',
           'Road':'Road',      
           'Street': 'Street',
           'Avenue': 'Avenue',
           'Drive': 'Drive',
           'Boulevard':'Boulevard',
           'Parkway': 'Parkway',
           'Place': 'Place',
           'Court': 'Court',
           'Trail': 'Trail',
           'Lane': 'Lane'
           }

def update_name(name, mapping):
    '''Update each street name with the replacement ending in the mapping dictionary'''
    match = re.search(street_type_re,name)
    if match:
        name = re.sub(street_type_re,mapping[match.group()],name)
    return name

#file_in = 'GVRD - Vancouver - OSM XML Raw.osm' 
#file_in = 'sample.osm'
file_in = 'example.osm'

def shape_element(element):
    """Takes a top level element or tag such as way, node, etc and iterates through each element
    and 2nd level tag (if applicable). Returns one cleaned
    node (could be a 'way' as well) which is a dictionary of all the fields later 
    to be converted to a JSON document.    
    """
    if element.tag == "node" or element.tag == "way":
        node = {} #variable is called node, but it can also be a way
        #1st level tags
        node['type'] = element.tag          
        for attrName, attrValue in element.attrib.items(): #iterate through each 1st level attributes of tag 'node' or 'way'
            if attrName == "lat":
                if 'pos' not in node.keys():
                    node['pos']= [float(1),float(1)]
                node['pos'][0] = float(attrValue)
                continue
            if attrName == "lon":
                if 'pos' not in node.keys():
                    node['pos']= [float(1),float(1)]
                node['pos'][1] = float(attrValue)
                continue
            if attrName == "" or attrValue == "": #avoid importing any blank keys or values
                continue
            if attrName == 'id': #id is a first level attribute
                node['_id'] = attrValue #doing this ensures this _id replaces ObjectId in mongoDB when importing
                continue
            node[attrName] = attrValue
        #2nd level tags
        ndtags = element.findall("./*")
        for ndtag in ndtags: #iterate through each 2nd level tag
            kvalue, vvalue, refvalue = ['','','']
            for aName, aValue in ndtag.attrib.items(): #iterate through each tag to extract all 3 possible attributes 
                if aName == "k":
                    kvalue = aValue
                if aName == "v":
                    vvalue = aValue
                if aName == "ref":
                    refvalue = aValue
            if kvalue == 'type': #there are some values that already have a type - this ensures only way and node types are not overridden
                continue
            dc,pc,lc = [double_colon.search(kvalue),problemchars.search(kvalue),lower_colon.search(kvalue)]
        
        #if second level tag "k" value contains problematic characters, it should be ignored
            if pc or dc: #bitcoin=yes & contact"email from tags.py and ignore double colons
                continue 
            if vvalue in skip:# it is one of the skipped words found in the audit:
                continue
            if vvalue in changes: #it is one of the words we need to rename for various reasons typos, extra spaces etc.
                vvalue = changes[vvalue]
            if kvalue.startswith("addr:"):
                if kvalue == "addr:street": #same as "is a street" function from audit.py
                    vvalue = update_name(vvalue, mapping)         
                if 'address' not in node.keys(): #this would be the first tag if there are multiple tags               
                    node['address'] = {}
                node['address'][kvalue.split("addr:")[1]] = vvalue #pick the second item[0,1] out of this split k value which is for example 'street'         
                continue
            if lc: #if any all lower character fields with a colon in them 
                kvalue = re.sub(":"," ",kvalue) #replace the colon with an space
                node[kvalue] = vvalue
                continue
            if kvalue.startswith("geobase:"): #example geobase:acquisitionTechnique - lower_colon byitself is not good enough because capital "T"            
                kvalue = kvalue.split("geobase:")[1] #remove the geobase section
                node[kvalue] = vvalue
                continue                
            if kvalue == "" or vvalue == "": #avoid blank fields and values
                continue
            if element.tag == "way" and refvalue != "" : #if it is a 'way' and references 'nodes'  
                if "node_refs" not in node.keys():
                    node['node_refs'] = []
                node["node_refs"].append(refvalue)
            node[kvalue] = vvalue
        node["orig_numFields"] = len(node.keys()) #added this so I can see in MongoDB how many documents have only 3 keys id, pos, and type
        return node
    else:
        return None

def process_map(file_in, pretty = False):    
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    counter = 0 #added counter to show status when creating json file
    with codecs.open(file_out, "w") as fo:        
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            counter += 1
            print counter
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
      
data = process_map(file_in, False)

#len(data) = 1538286 unique nodes and ways
#4197699 total elements(any type of 1st level tag)
#imported all elements succesfully into mongoDB
