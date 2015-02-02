"""
Created on Fri Jan 30 01:34:32 2015

@author: user
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

import os
#Set the proper current working directory
os.getcwd()
os.chdir('C:/Users/user/version-control/Project-2-Data-Wrangling-with-MongoDB')

OSMFILE = "GVRD - Vancouver - OSM XML Raw.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE           
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
           }
#gotten from looking at the results of the audit
#difference between mapping and changes is we are looking at the entire value in changes and not just the last word. see data.py
#changes = { 'ing George Hwy.': 'King George Boulevard',
#           'W15th st': 'W 15th Street',
#           'Howe St. Vancouver': 'Howe Street',
#           'W. Hastings St. Vancouver': 'West Hastings Street',
#           'Expo Blvd, #3305': 'Expo Boulevard'            
#           ' Beatty St': 'Beatty Street'}         
##skip are the full values gotten from looking at the results of the audit that we don't want to include in the database. Will use in data.py
#skip = ["10","32500","99","Tsawwassen","Park","Terminal","8500"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    elem.clear() #clear from memory
    return street_types

def update_name(name, mapping):
    '''Update each street name with the replacement ending in the mapping dictionary'''
    match = re.search(street_type_re,name)
    name = re.sub(street_type_re,mapping[match.group()],name)
    return name

st_types = audit(OSMFILE)
pprint.pprint(dict(st_types))

for st_type, ways in st_types.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        print name, "=>", better_name

