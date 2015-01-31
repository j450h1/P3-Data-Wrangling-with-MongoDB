"""
Created on Fri Jan 30 01:34:32 2015

@author: user
"""

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

import os
#Set the proper current working directory
os.getcwd()
os.chdir('C:/Users/user/version-control/Data-Wrangle-OpenStreetMaps-MongoDB')

OSMFILE = "GVRD - Vancouver - OSM XML Raw.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
#mapping = { "St.": "Street",
#            "St": "Street",
#            "st": "Street",
#            "street": "Street",
#            "Street3": "Street",
#            "Blvd": "Boulevard",            
#            "Ave": "Avenue",
#            "RD": "Road",
#            "Rd": "Road",
#            "Rd.": "Road",
#            "road": "Road",
#            "Road,": "Road",
#            "Dr": "Drive",
#            "Dr.": "Drive",
#            "Ave.": "Avenue", # combined all Avenues
#            "av" : "Avenue",
#            "S.": "South",
#            "Hwy.": "Highway",
#            "Hwy": "Highway",            
#            "Edmonds": "Edmonds Street",
#            "Hastings": "Hastings Street",
#            "Willingdon" : "Willingdon Avenue",
#            "Pender": "Pender Street",
#            "Moncton": "Moncton Street",
#            "77A": "77A Avenue" 
#            }
           
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
           'Sanders': 'Sanders',
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
#must be done After the street name changes above. 
changes = { 'ing George Highway': 'King George Boulevard',
           'W15th Street': 'W 15th Street',
           'Howe St. Vancouver': 'Howe Street',
           'W. Hastings St. Vancouver': 'West Hastings Street',
           'Expo Blvd, #3305': 'Expo Boulevard'            
            }         
            
delete = ["Tsawwassen","Park","Terminal","Sanders","8500"]

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

def change_name(name, changes):
    match = re.search(street_type_re,name)
    name = re.sub(street_type_re,mapping[match.group()],name)
    return name

def delete_name(name, delete):
    match = re.search(street_type_re,name)
    name = re.sub(street_type_re,mapping[match.group()],name)
    return name

st_types = audit(OSMFILE)
pprint.pprint(dict(st_types))

for st_type, ways in st_types.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        print name, "=>", better_name

