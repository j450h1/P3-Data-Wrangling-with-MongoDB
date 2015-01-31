# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 01:28:21 2015

@author: user
"""
import xml.etree.ElementTree as ET
import pprint

"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""
import os
#Set the proper current working directory
os.getcwd()
os.chdir('C:/Users/user/version-control/Project-2-Data-Wrangling-with-MongoDB')

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        try:
            users.add(element.attrib['uid'])
        except KeyError:
            pass
        element.clear() #to clear memory
    return users

users = process_map('GVRD - Vancouver - OSM XML Raw.osm')
pprint.pprint(users)
#RESULT set([])
#no users have contributed
#however attributed, created_by, and source may have some useful information by examining the OSM file

import send_text_message
message = "Python script is complete. Get back to the computer!"
send_text_message.send_text(message)
