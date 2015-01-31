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
           'Road':'Road',      #avoid keyerror for not having existing value
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
    name = re.sub(street_type_re,mapping[match.group()],name)
    return name
#
#file_in = 'GVRD - Vancouver - OSM XML Raw.osm'
#data = list()
#counter = 0
##skip_counter = 0    
##len(data) = 1538286 unique nodes and ways
##4197699 total elements
#for _, element in ET.iterparse(file_in):
#    if element.tag == "node" or element.tag == "way":
#        node = {}
#        node['pos'] = [float(1),float(1)]
#        node['type'] = element.tag          
#        for attrName, attrValue in element.attrib.items():
#            if attrName == "lat" or attrName == "lon": #pos
#                if attrName == "lat":
#                    node['pos'][0] = float(attrValue)
#                if attrName == "lon":
#                    node['pos'][1] = float(attrValue)            
#            if attrName == "" or attrValue == "": #make sure no empty tags get copied over 
#                    continue
#            node[attrName] = attrValue
#        #2nd level 'nd' or 'tag' tags     
#        ndtags = element.findall("./*")        
#        for ndtag in ndtags:
#            kvalue, vvalue, refvalue, refname = ["","","",""]
#            for aName, aValue in ndtag.attrib.items():
#                if aName == "k":
#                    #print "k"
#                    kvalue = aValue
#                if aName == "v":
#                    #print "v"
#                    vvalue = aValue
#                if aName == "ref":
#                    refvalue = aValue
#                    refname = aName #should be 'ref'
##            #print "2nd level"  
##            print kvalue
##            print vvalue
##            print refvalue
#            dc = double_colon.search(kvalue)
#            pc = problemchars.search(kvalue)
#            #if second level tag "k" value contains problematic characters, it should be ignored
#            if pc is not None or dc is not None: #bitcoin=yes & contact"email from tags.py and ignore double colons
#                print "pced or dced"                
#                continue 
#            if vvalue in skip:# it is one of the skipped words found in the audit:
#                print "skipped"                
#                continue
#            if vvalue in changes: #it is one of the words we need to rename for various reasons typos, extra spaces etc.
#                print "changed"                
#                vvalue = changes[vvalue]
#            if kvalue.startswith("addr:"):
#                #Change all street endings to the better name
#                if kvalue == "addr:street": #is a street function from audit
#                    vvalue = update_name(vvalue, mapping)
#                if 'address' not in node.keys(): #this would be the first tag if there are multiple tags               
#                    node['address'] = {}
#                node['address'][kvalue.split("addr:")[1]] = vvalue #pick the second item[0,1] out of this split k value which is for example 'street' 
#            elif element.tag == "way" and refname == "ref": #if it is a way and references nodes
#                if "node_refs" not in node.keys():
#                    node['node_refs'] = []
#                print "reffed"
#                node["node_refs"].append(refvalue)
#            else: #this is executed for both ways and nodes
#                if kvalue == "" or vvalue == "": #make sure no empty tags get copied over 
#                    continue
#                node[kvalue] = vvalue
#                print kvalue 
#                print vvalue 
#                print refvalue
#                print refname 
#        data.append(node)
#    #    counter += 1
#    #   print counter #gives an idea of the progress of the task
#    element.clear()

def shape_element(element):
    if element.tag == "node" or element.tag == "way":
        node = {}
        node['pos'] = [float(1),float(1)]
        node['type'] = element.tag          
        for attrName, attrValue in element.attrib.items():
            if attrName == "lat" or attrName == "lon": #pos
                if attrName == "lat":
                    node['pos'][0] = float(attrValue)
                if attrName == "lon":
                    node['pos'][1] = float(attrValue)            
            if attrName == "" or attrValue == "": #make sure no empty tags get copied over 
                    continue
            node[attrName] = attrValue
        #2nd level 'nd' or 'tag' tags     
        ndtags = element.findall("./*")        
        for ndtag in ndtags:
            kvalue, vvalue, refvalue, refname = ["","","",""]
            for aName, aValue in ndtag.attrib.items():
                if aName == "k":
                    #print "k"
                    kvalue = aValue
                if aName == "v":
                    #print "v"
                    vvalue = aValue
                if aName == "ref":
                    refvalue = aValue
                    refname = aName #should be 'ref'
#            #print "2nd level"  
#            print kvalue
#            print vvalue
#            print refvalue
            dc = double_colon.search(kvalue)
            pc = problemchars.search(kvalue)
            #if second level tag "k" value contains problematic characters, it should be ignored
            if pc or dc: #bitcoin=yes & contact"email from tags.py and ignore double colons
                print "pced or dced"                
                continue 
            if vvalue in skip:# it is one of the skipped words found in the audit:
#                print "skipped"                
                continue
            if vvalue in changes: #it is one of the words we need to rename for various reasons typos, extra spaces etc.
#                print "changed"                
                vvalue = changes[vvalue]
            if kvalue.startswith("addr:"):
                #Change all street endings to the better name
                if kvalue == "addr:street": #is a street function from audit
                    vvalue = update_name(vvalue, mapping)
                if 'address' not in node.keys(): #this would be the first tag if there are multiple tags               
                    node['address'] = {}
                node['address'][kvalue.split("addr:")[1]] = vvalue #pick the second item[0,1] out of this split k value which is for example 'street' 
            elif element.tag == "way" and refname == "ref": #if it is a way and references nodes
                if "node_refs" not in node.keys():
                    node['node_refs'] = []
#                print "reffed"
                 node["node_refs"].append(refvalue)
            else: #this is executed for both ways and nodes
                if kvalue == "" or vvalue == "": #make sure no empty tags get copied over 
                    continue
                node[kvalue] = vvalue
#                print kvalue 
#                print vvalue 
#                print refvalue
#                print refname 
        return node
    else:
        return None

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    counter = 0
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
            element.clear()
    return data

data = process_map('GVRD - Vancouver - OSM XML Raw.osm', False)
pprint.pprint(data)

