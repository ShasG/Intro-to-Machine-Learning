
# coding: utf-8

# #             OpenStreetMap Data Wrangling Project with SQL

# 
# ### Map Area: 
# I have extracted OSM file from openstreemap.org and it is for my residential area 'Milwaukee County'. Total this file is more than 2GB, hence I have reduced the area locality to get a smaller size of file which is around 150 MB. I am interested to know more about my area through this project and want to see what reveals about my locality via query.
# 
# We will now go through the data wrangling process.
# 

# In[1]:

#Import all the required modules
import xml.etree.cElementTree as ET
from collections import defaultdict as dfdict
import re
import pprint
import os
import sqlite3
import csv
import codecs
import pandas as pd
import math
import schema
import cerberus


# In[2]:

#The OSM file path
OSM_PATH = "C:\Udacity\Nano degree\Core Curriculam 4_Data Wrangling\Project\Milwaukee_Map.osm"


# In[3]:

#Getting the file size
os.path.getsize(OSM_PATH)


# In[4]:

#Convert the size to MB
def convert_size(size):
    if (size == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p,2)
    return '%s %s' % (s,size_name[i])

print(convert_size(os.path.getsize(OSM_PATH)))


# ###### Creating sample file with the k – th size and storing it as 'milwaukee_sample.osm'

# In[5]:

SAMPLE_FILE = "milwaukee_sample.osm"

k = 15 # Every k-th top level element
def get_element_1(osm_file, tags=('node', 'way', 'relation')):
    
    context = iter(ET.iterparse(OSM_PATH, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

with open(SAMPLE_FILE, 'wb') as output:
    b = bytearray()
    b.extend('<?xml version="1.0" encoding="UTF-8"?>\n'.encode())
    b.extend('<osm>\n  '.encode())
    output.write(b)

    # Write every kth top level element
    print (OSM_PATH)
    for i, element in enumerate(get_element_1(OSM_PATH, tags=('node', 'way', 'relation'))):

        if not i % k:
            output.write(ET.tostring(element, encoding='utf-8'))
    b_end = bytearray()
    b_end.extend('</osm>'.encode())
    output.write(b_end)


# In[6]:

#Find the size of sample file
SAMPLE_PATH = "C:\Udacity\Nano degree\Core Curriculam 4_Data Wrangling\Project\milwaukee_sample.osm"
print(convert_size(os.path.getsize(SAMPLE_PATH)))


# Now going through the OSM file to find out wha informations are there. First finding the total 'TAG' present in the file and it's type.

# In[5]:

# Function for counting tags
def count_tags(filename):
    count = dfdict(int)
    for item in ET.iterparse(filename):
        count[item[1].tag] += 1
    return count


# In[92]:

#Get the TAG details
count_tags(OSM_PATH)


# In[6]:

#Count UNIQUE user ID in the file
def count_uid(file_name):
    uids = set()
    tags_with_uids = ['node', 'way', 'relation']
    for _,item in ET.iterparse(file_name):
        if item.tag in tags_with_uids:
            uid = item.attrib['uid']
            if uid in uids:
                pass
            else:
                uids.add(uid)
    return uids


# In[43]:

#Find the user count
print(len(count_uid(OSM_PATH)))


# Creating a dictionary having the UID and user name 

# In[7]:

#Find the user name for all the user ids
def user_details(filename):
    users = {}
    tags_with_uids = ['node', 'way', 'relation']
    for _, element in ET.iterparse(filename):

        if element.tag in tags_with_uids:
            user =  {element.attrib['uid']: element.attrib['user']}
            users.update(user)
    return users


# In[96]:

user_details = user_details(OSM_PATH) 
print(len(user_details)) 


# In[98]:

#Print the user name and its id
pprint.pprint(dict(user_details))


# ###### Now populating all the address attribute to find what are the inconsistency or wrong value present in map

# In[3]:

#Function for counting address attributes by type
def find_all_addr_attr_count(filename):
    address_attr = {}
    tag_with_addr = ['node', 'way']
    for event, elem in ET.iterparse(filename):
        if elem.tag in tag_with_addr:           #== "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if re.search(re.compile("addr:.*$"),tag.get("k")):
                    if tag.get("k") in address_attr:
                        address_attr[tag.get("k")]+=1
                    else:
                        address_attr[tag.get("k")]=1
    return address_attr


# In[9]:

#Get the address attributes by type
find_all_addr_attr_count(OSM_PATH)


# Above are the types of different address attributes found in the given file.

# In[4]:

#Function to get all the different values for a given attribute type
def find_attr_values(filename,attr):
    final = str(attr)
    address_attr = {}
    tag_with_addr = ['node', 'way']
    for event, elem in ET.iterparse(filename):
        if elem.tag in tag_with_addr:           #== "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if re.search(re.compile(final),tag.get("k")):
                    if tag.get("v") in address_attr:
                        address_attr[tag.get("v")]+=1
                    else:
                        address_attr[tag.get("v")]=1
    return address_attr


# In[11]:

print(len(find_attr_values(OSM_PATH,"addr:city")))


# In[12]:

#Finding the city name with their frequency
find_attr_values(OSM_PATH,"addr:city") 


# There are total 41 different types of city name has been used. All of these are not part of Milwaukee County, the file also includes some part of other crossing counties.
# 
# ###### Now going to check on street address.

# In[13]:

#Finding the street names in the file
find_attr_values(OSM_PATH,"addr:street")


# In[5]:

#Finding the street names in the file
find_attr_values(OSM_PATH,"addr:postcode")


# We can see from above postal code values, that most of them are with 5 digits pattern. But few are with extra 4 digits extension and few are with state name. Will convert all of them in same 5 digits format.
