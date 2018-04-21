
# coding: utf-8

# ### Correct the data and save it in CSV file

# In[1]:

#Importing from custom module in jupyter notebook
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)


# In[2]:

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
import sys


# In[3]:

#This module is doing the audit and correction of phone numbers
from OSDM import AuditPhone as ap
#This module is doing the audit and correction of postal code
from OSDM import AuditPostcode as apc
#This module is doing the audit and correction of street name
from OSDM import AuditStreet as ast


# In[4]:

#The OSM file path
OSM_PATH = "C:\Udacity\Nano degree\Core Curriculam 4_Data Wrangling\Project\Milwaukee_Map.osm"


# In[5]:

#CSV file name which will be created during next part
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# Strings with lower case chars and a ':'
LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
# Strings with chars that will cause problems as keys.
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


# In[6]:

#Transforms the XML data into specified format as a list of Python dictionaries.
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements    
    
    if element.tag == 'node':
        for item in NODE_FIELDS:    #adding the header row
            node_attribs[item] = element.attrib[item]
            
        for tag in element.iter('tag'):
            problem = PROBLEMCHARS.search(tag.attrib['k'])
            if not problem:

                name = tag.attrib["v"]
                #Correction for STREET name
                if ast.is_street_name(tag):
                    #Correcting street name prefix(like st., rd, ln) to proper one
                    m = ast.street_type_regex_post.search(name)
                    if m:
                        street_type = m.group()
                        if street_type not in ast.expected_post:
                            name = ast.update_name(name,ast.mapping_street_post,ast.street_type_regex_post)
                                                        
                    #Correcting street name prefix(like N., S, W.) to proper one        
                    m1 = ast.street_type_regex_pre.search(name)
                    if m1:
                        street_type1 = m1.group()
                        if street_type1 not in ast.expected_pre:
                            name = ast.update_name(name,ast.mapping_street_pre,ast.street_type_regex_pre)
                            
                #Correction for zip code            
                if apc.is_zip_code(tag): #tag.attrib['k'] == "addr:postcode":
                    name = apc.postcode_correction(name)
                        
                #Correction for phone numbers
                if ap.is_phone_num(tag): #tag.attrib['k'] == "phone":
                    name = ap.update_phone(name)
                                
                ###
                node_tag_dictionary = {} 
                node_tag_dictionary['id'] = element.attrib['id'] 
                node_tag_dictionary['value'] = name #tag.attrib['v'] 
                
                point = LOWER_COLON.search(tag.attrib['k'])
                if not point:
                    node_tag_dictionary['type'] = 'regular'
                    node_tag_dictionary['key'] = tag.attrib['k']
                else:
                    before = re.findall('^(.+):', tag.attrib['k'])
                    after = re.findall('^[a-z]+:(.+)', tag.attrib['k'])
                    
                    if before:
                        node_tag_dictionary['type'] = before[0]
                    if after:   #got one indexing error at below line. hence checking if 'after' is not initial
                        node_tag_dictionary['key'] = after[0]
                    
            tags.append(node_tag_dictionary)
        #print (node_attribs, tags)
        return {'node': node_attribs, 'node_tags': tags}
            
                         
    elif element.tag == 'way':   
        for item in WAY_FIELDS:    #adding the header row
            way_attribs[item] = element.attrib[item]
    
        for tag in element.iter('tag'):  
 
            problem = PROBLEMCHARS.search(tag.attrib['k'])
            if not problem:
            
                name = tag.attrib["v"]
                #Correction for STREET name
                if ast.is_street_name(tag):
                    #Correcting street name prefix(like st., rd, ln) to proper one
                    m = ast.street_type_regex_post.search(name)
                    if m:
                        street_type = m.group()
                        if street_type not in ast.expected_post:
                            name = ast.update_name(name,ast.mapping_street_post,ast.street_type_regex_post)
                            
                    #Correcting street name prefix(like N., S, W.) to proper one        
                    m1 = ast.street_type_regex_pre.search(name)
                    if m1:
                        street_type1 = m1.group()
                        if street_type1 not in ast.expected_pre:
                            name = ast.update_name(name,ast.mapping_street_pre,ast.street_type_regex_pre) 
                            
                #Correction for zip code            
                if apc.is_zip_code(tag): #tag.attrib['k'] == "addr:postcode":
                    name = apc.postcode_correction(name)
                        
                #Correction for phone numbers
                if ap.is_phone_num(tag): #tag.attrib['k'] == "phone":
                    name = ap.update_phone(name)
                            
                ###  
                way_tag_dictionary = {}
                way_tag_dictionary['id'] = element.attrib['id'] 
                way_tag_dictionary['value'] = name #tag.attrib['v']  

                point = LOWER_COLON.search(tag.attrib['k'])
                if not point:
                    way_tag_dictionary['type'] = 'regular'
                    way_tag_dictionary['key'] = tag.attrib['k']
                else:
                    before = re.findall('^(.+):', tag.attrib['k'])
                    after = re.findall('^[a-z]+:(.+)', tag.attrib['k'])

                    if before:
                        way_tag_dictionary['type'] = before[0].split(':')[0] #to split at ':' where more than one ':' is in value
                    if after:
                        way_tag_dictionary['key'] = after[0]

            tags.append(way_tag_dictionary)
            
        count = 0    
        for tag in element.iter("nd"):  
            way_nd_dictionary = {} 
            way_nd_dictionary['id'] = element.attrib['id'] 
            way_nd_dictionary['node_id'] = tag.attrib['ref'] 
            way_nd_dictionary['position'] = count  
            count += 1
            
            way_nodes.append(way_nd_dictionary)
            
        #print (way_attribs, way_nodes, tags)
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}                      


# In[7]:

#Find the element with right type of TAG
def get_element(osm_file, tags=('node', 'way', 'relation')):
    
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


# In[8]:

#Extend csv.DictWriter to handle Unicode input
class UnicodeDictWriter(csv.DictWriter, object):
    
    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# In[9]:

#Iteratively process each XML element and write to csv
def process_map(file_in):
        
    with    codecs.open(NODES_PATH, 'w') as nodes_file,             codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,             codecs.open(WAYS_PATH, 'w') as ways_file,             codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,             codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file :

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()
        
        
        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])                    


# In[10]:

if __name__ == '__main__':
    process_map(OSM_PATH)


# CSV files have been generated.
