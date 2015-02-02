# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 23:21:48 2015

@author: user
"""
import xml.etree.ElementTree as ET
import pprint
import re

import os
#Set the proper current working directory
os.getcwd()
os.chdir('C:/Users/user/version-control/Project-2-Data-Wrangling-with-MongoDB')

#create the three regular expressions we are checking for
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        if re.search(lower, element.attrib['k']):        
            keys['lower'] += 1            
        elif re.search(lower_colon, element.attrib['k']):
            keys['lower_colon'] += 1            
        elif re.search(problemchars, element.attrib['k']):
            keys['problemchars'] += 1
            #print out any values with problematic characters
            #print element            
            print element.attrib['k']            
        else:
            keys['other'] += 1                 
    
    return keys

def process_map(filename):
    #initialize dictionary
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        # discard the element is needed to clear from memory and speed up processing
        element.clear()
    return keys

keys = process_map('GVRD - Vancouver - OSM XML Raw.osm')
pprint.pprint(keys)

#RESULT
#bitcoin=yes
#contact"email
#Will ignore these two problemchars in 5. data.py
#{'lower': 574368, 'lower_colon': 448514, 'other': 44552, 'problemchars': 2}